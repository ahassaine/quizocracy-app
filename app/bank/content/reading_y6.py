"""Reading comprehension, Year 6 (keys RD6.01-RD6.16): 16 passages of 300-450 words, 7 questions each.

Spec: app/bank/SPEC_READING.md (and SPEC.md for the question format). Every passage and question is
original writing, written by hand, to prepare for the KS2 SATs reading paper: questions are phrased the way
the paper asks them ("Find and copy...", "Which word is closest in meaning to...", "Why did the writer...",
"Using information from the text...", "Which of these is a fact, not an opinion?").

Topics link to the Year 6 curriculum where natural: a biography of Louis Braille (how braille was
invented), the circulatory system and keeping healthy, light and how we see, electrical circuits,
classification, the Second World War home front (an evacuee's letters: evacuation and rationing), the Maya
number system and cities, climate zones and mountains, coastal erosion (a news report); plus stories (starting
secondary school, suspense without horror, a moral dilemma, a sports final), a poem, a balanced argument
(school uniform) and a persuasive leaflet (Walk to School Week).

The questions cover every KS2 reading domain (retrieve, infer, vocab, sequence, summarise, structure,
language, compare, predict, purpose), retrieval and inference most often. To be checked line by line by a
second reviewer (facts, one defensible answer per question, no leaks) before scripts/bank_ids.py gives the
questions their ids.
"""

SKILLS = [
    {
        "key": "RD6.01",
        "year": 6,
        "strand": "Stories",
        "title": "The map in the margin",
        "nc": "Draw inferences such as inferring characters' feelings, thoughts and motives from their actions",
        "text": (
            "Mateus had walked past Kingsmead Academy hundreds of times, but he had never been inside. Now, on a "
            "grey September morning, he stood at the gates in a blazer that still had creases from the packet, and "
            "the building seemed to have grown overnight.\n\n"
            "“Year 7s, this way!” called a woman with a lanyard full of keys. Mateus followed a river of identical "
            "blazers into the hall, where he searched the rows for anyone from Brook Lane Primary. There was no one. "
            "His best friend, Callum, had gone to a school on the other side of the city, and the silence where "
            "Callum's jokes should have been felt enormous.\n\n"
            "His timetable was a grid of codes: Sc2, Ma4, Hu1. By the end of the second lesson, Mateus had climbed "
            "the wrong staircase twice and arrived at science so late that the only empty stool was next to a girl "
            "who was drawing tiny maps in the margin of her planner.\n\n"
            "“You're lost too?” she whispered.\n\n"
            "“Completely,” he admitted.\n\n"
            "“I'm Rosa. I've worked out that C block has two staircases and only one of them goes to the top floor. "
            "That's the trap.” She tapped her drawing. “I'm mapping the whole school.”\n\n"
            "At lunch, the canteen was a roar of trays and voices. Mateus hovered with his plate of pasta, his ears "
            "burning, until he spotted Rosa waving a fork at him from a corner table. Beside her sat a boy called "
            "Dev, who was trying to fold his timetable into a paper crane.\n\n"
            "“It's no use as a timetable,” Dev explained. “Nobody can read it anyway.”\n\n"
            "By the afternoon, the three of them had a system. Rosa navigated, Dev memorised the names of the "
            "teachers, and Mateus, who was good with numbers, worked out how many minutes they had to get from one "
            "room to the next. They were only late once, and that was because Dev stopped to rescue a crane that "
            "had fallen out of his pocket.\n\n"
            "When the final bell rang, Mateus's mum was waiting at the gate. “Well?” she asked, studying his face. "
            "“How was it?”\n\n"
            "Mateus thought about the staircase, the crowded hall and the noise of the canteen. Then he thought "
            "about the tiny maps.\n\n"
            "“Tomorrow,” he said, “I'm bringing a pen with three colours. Rosa needs one for the fire exits.”"
        ),
        "qs": [
            {"id": "5421aca79dc4", "t": "mcq", "d": "vocab", "q": "“Mateus followed a river of identical blazers into the hall.” Which word is closest in meaning to identical?",
             "opts": ["exactly alike", "brand new", "very smart", "far too big"],
             "why": "Identical means exactly the same: every new pupil was wearing the same blazer."},
            {"id": "06d2e91dce94", "t": "mcq", "d": "infer", "q": "“The silence where Callum's jokes should have been felt enormous.” What does this suggest about Mateus?",
             "opts": ["He missed his friend and felt alone.",
                      "He was glad that the hall was so quiet.",
                      "He was cross that Callum had not come.",
                      "He was worried about telling jokes."],
             "why": "He looked for someone he knew and found no one; the gap left by Callum's jokes shows how much he missed his friend."},
            {"id": "b53ae7f54d23", "t": "text", "d": "retrieve", "q": "What was Rosa drawing in the margin of her planner? Find and copy two words.",
             "a": ["tiny maps", "maps", "tiny map", "map"],
             "why": "The third paragraph says she was drawing tiny maps in the margin of her planner."},
            {"id": "028f17fd03ec", "t": "tap", "d": "language", "q": "Tap the word that shows how loud the canteen was.",
             "s": "At lunch, the canteen was a [roar] of trays and voices.",
             "why": "A roar is a very loud, deep noise, so the word shows the canteen was extremely noisy."},
            {"id": "b831ff06621a", "t": "mcq", "d": "infer", "q": "Why were Mateus's ears burning as he hovered with his plate?",
             "opts": ["He felt embarrassed because he had nowhere to sit.",
                      "The pasta on his plate was far too hot to hold.",
                      "He had run all the way from the science room.",
                      "Rosa and Dev were laughing at him from a table."],
             "why": "He hovered, not knowing where to go, until Rosa waved: burning ears are a sign of feeling embarrassed and awkward."},
            {"id": "37eadf84233d", "t": "mcq", "d": "retrieve", "q": "Using information from the text, what was Mateus's job in the group's system?",
             "opts": ["working out the minutes between lessons",
                      "remembering the names of the teachers",
                      "drawing maps of each floor of the school",
                      "finding the quickest staircase to use"],
             "why": "Mateus was good with numbers, so he worked out how many minutes they had to get from one room to the next."},
            {"id": "36dacd510716", "t": "mcq", "d": "predict", "q": "Using the ending, what is Mateus most likely to do tomorrow?",
             "opts": ["help Rosa add to her map of the school",
                      "ask to move to Callum's school instead",
                      "sit on his own at lunch in the canteen",
                      "fold his timetable into a paper crane"],
             "why": "He plans to bring a three-colour pen because Rosa needs one for the fire exits: he means to help with her map."},
        ],
    },
    {
        "key": "RD6.02",
        "year": 6,
        "strand": "Information",
        "title": "The body's delivery service",
        "nc": "Retrieve, record and present information from non-fiction",
        "text": (
            "Every minute of every day, without you ever having to think about it, a remarkable delivery service "
            "is at work inside your body. It is called the circulatory system, and it has three main parts: the "
            "heart, the blood vessels and the blood itself.\n\n"
            "The heart is a muscle about the size of your clenched fist, and it sits in your chest, slightly to "
            "the left. Its job is to pump. Each time it squeezes, it pushes blood out through tubes called blood "
            "vessels. When it relaxes, it fills up with blood again. This squeeze and relax is your heartbeat, and "
            "you can feel it as a pulse in your wrist or your neck.\n\n"
            "The heart is really two pumps side by side. The right side sends blood to the lungs, where the blood "
            "picks up oxygen from the air you have breathed in and gets rid of carbon dioxide, a waste gas that you "
            "then breathe out. The blood, now rich in oxygen, travels back to the left side of the heart, which "
            "pumps it out to the rest of the body.\n\n"
            "There are three kinds of blood vessel. Arteries carry blood away from the heart. Veins carry blood "
            "back towards it. Joining them are capillaries, which are so narrow that blood cells have to pass "
            "through them in single file. It is through the thin walls of the capillaries that oxygen reaches "
            "every part of you.\n\n"
            "Blood does more than carry oxygen. It also transports water and nutrients from your digested food to "
            "the cells that need them, and it collects waste to be removed from the body. Without this constant "
            "delivery, your muscles could not move and your brain could not think.\n\n"
            "Like any muscle, the heart becomes stronger when it is exercised. Activities that make you slightly "
            "out of breath, such as running, swimming or cycling, make the heart work harder, and over time it "
            "becomes better at pumping. A balanced diet helps too, while smoking damages the heart and blood "
            "vessels and makes the whole system work less well.\n\n"
            "So the next time you race across the playground and feel your heart thumping, remember that it is "
            "simply doing its job: delivering what your body needs, one beat at a time."
        ),
        "qs": [
            {"id": "08f74e6fbec6", "t": "text", "d": "retrieve", "q": "What does the writer compare the size of the heart to? Find and copy.",
             "a": ["your clenched fist", "clenched fist", "a clenched fist", "fist", "your fist"],
             "why": "The second paragraph says the heart is a muscle about the size of your clenched fist."},
            {"id": "d6181172819b", "t": "mcq", "d": "language", "q": "Why does the writer call the circulatory system “a remarkable delivery service”?",
             "opts": ["It carries what the body needs to every part, like deliveries to homes.",
                      "It is run by workers who drive vans around the inside of the body.",
                      "It only works when you think about it, like ordering a parcel.",
                      "It moves food from your plate into your mouth and stomach."],
             "why": "The text explains that blood carries oxygen, water and nutrients to the cells that need them, just as a delivery service brings things to where they are needed."},
            {"id": "e1017b374058", "t": "mcq", "d": "retrieve", "q": "According to the text, which side of the heart pumps blood to the lungs?",
             "opts": ["the right side", "the left side", "both sides together", "the top of the heart"],
             "why": "The third paragraph says the right side sends blood to the lungs; the left side pumps it to the rest of the body."},
            {"id": "ff82ee36ae2f", "t": "tap", "d": "vocab", "q": "Tap the word that means “carries from one place to another”.",
             "s": "It also [transports] water and nutrients from your digested food to the cells that need them, and it collects waste to be removed from the body.",
             "why": "To transport something is to carry it from one place to another."},
            {"id": "040968dc9867", "t": "mcq", "d": "compare", "q": "Using information from the text, how are arteries different from veins?",
             "opts": ["Arteries carry blood away from the heart; veins carry it back.",
                      "Arteries are so narrow that blood cells must go in single file.",
                      "Arteries carry food to the cells; veins carry only oxygen.",
                      "Arteries are found in the chest; veins are found in the arms."],
             "why": "The fourth paragraph says arteries carry blood away from the heart and veins carry it back towards it. The single-file vessels are capillaries."},
            {"id": "357f4b871457", "t": "mcq", "d": "infer", "q": "Using the text, why might a smoker get out of breath more easily than a non-smoker?",
             "opts": ["Smoking harms the parts that carry blood around the body.",
                      "Smoking makes the heart grow larger than a fist.",
                      "Smoking stops the blood from carrying any water.",
                      "Smoking makes the capillaries far too wide."],
             "why": "The sixth paragraph says smoking damages the heart and blood vessels and makes the whole system work less well, so less oxygen gets around the body."},
            {"id": "a88ce28da190", "t": "mcq", "d": "summarise", "q": "Which would be the best subheading for the paragraph that begins “Like any muscle”?",
             "opts": ["Keeping your heart healthy", "Two pumps side by side",
                      "Three kinds of blood vessel", "What blood carries"],
             "why": "That paragraph is about exercise, diet and smoking: how to keep the heart strong and healthy."},
        ],
    },
    {
        "key": "RD6.03",
        "year": 6,
        "strand": "Letters and diaries",
        "title": "Letters from an evacuee",
        "nc": "Draw inferences and justify them with evidence from the text; identify how a writer's feelings change",
        "text": (
            "Hollow Brook Farm\nnear Tavistock, Devon\n5th September 1939\n\n"
            "Dear Mum,\n\n"
            "We got here safe, so please do not worry. The train took nearly all day, and a kind lady who was "
            "travelling with us gave us each a paper bag with a bun and an apple in it. I still have my gas mask in "
            "its cardboard box, and the label with my name on is tied to my coat button, just like you did it.\n\n"
            "When we got off the train they took us to a village hall, and the farmers and their wives came to "
            "choose who they would take. It was like being picked for football, only worse, because Georgie and I "
            "were nearly the last ones left. In the end Mrs Hext said she would have the both of us. She is tall "
            "and does not smile much, but she gave us hot cocoa before bed.\n\n"
            "There are cows here, Mum, real ones, and they are much bigger than they look in books. Georgie is "
            "scared of them. I am not, much.\n\n"
            "Please give Nan my love and tell her I am keeping my socks dry.\n\n"
            "Your loving son,\nArthur\n\n"
            "Hollow Brook Farm\n14th February 1940\n\n"
            "Dear Mum,\n\n"
            "Thank you for the parcel and the pencils. Mrs Hext says rationing has started properly now and "
            "everyone has a ration book, even us. She keeps ours in the dresser drawer and takes them to the shop "
            "in the village. We only get a little butter and sugar each week, but on the farm there are always "
            "eggs, so I think we are luckier than you are in London.\n\n"
            "I can milk a cow now! Mr Hext showed me how, and the first time I got more on my boots than in the "
            "bucket. Now I can fill half a pail. Even Georgie helps to feed the hens.\n\n"
            "Mrs Hext smiles more than she used to. Last night she let me help her make a pie with apples from the "
            "store, and she said I had a light hand with pastry, which I think is good.\n\n"
            "I still miss you and Nan and our street. But I don't cry at night any more. Will you come and visit "
            "when the weather is better? Mrs Hext says there is room.\n\n"
            "Your loving son,\nArthur"
        ),
        "qs": [
            {"id": "79ca8b5dbc05", "t": "mcq", "d": "retrieve", "q": "What did the kind lady on the train give the children?",
             "opts": ["a bun and an apple", "a cup of hot cocoa", "a label for their coat", "a parcel of pencils"],
             "why": "The first letter says she gave them each a paper bag with a bun and an apple in it."},
            {"id": "f626397a1eae", "t": "mcq", "d": "language", "q": "Arthur writes that being chosen “was like being picked for football, only worse”. What does this comparison show?",
             "opts": ["Waiting to be chosen made him feel unwanted.",
                      "He wished he could be playing football instead.",
                      "He thought choosing children was a fun game.",
                      "The farmers were rough with the children."],
             "why": "Being picked last for a team feels bad; he and Georgie were nearly the last left, so he felt nobody wanted them."},
            {"id": "26571e64d8d3", "t": "mcq", "d": "infer", "q": "“Georgie is scared of them. I am not, much.” What do the words “not, much” suggest?",
             "opts": ["Arthur is a little scared too but does not want to admit it.",
                      "Arthur has milked the cows many times before.",
                      "Arthur thinks the cows are smaller than in his books.",
                      "Arthur is laughing at Georgie for being frightened."],
             "why": "Adding “much” after “I am not” takes back part of what he said: he is a bit scared, though he plays it down."},
            {"id": "e18094f96912", "t": "text", "d": "retrieve", "q": "Where does Mrs Hext keep the children's ration books? Find and copy.",
             "a": ["in the dresser drawer", "the dresser drawer", "dresser drawer", "in the dresser", "the dresser"],
             "why": "The second letter says she keeps them in the dresser drawer."},
            {"id": "89d584d658b5", "t": "mcq", "d": "infer", "q": "Why does Arthur think he is luckier than his mum?",
             "opts": ["The farm has plenty of eggs, so he has more to eat.",
                      "He gets more butter and sugar than she does.",
                      "He does not need to have a ration book.",
                      "Mrs Hext buys him extra food at the shop."],
             "why": "He only gets a little butter and sugar like everyone else, but on the farm there are always eggs, so he has more food than people in London."},
            {"id": "5545f6a7af0a", "t": "mcq", "d": "compare", "q": "How has Mrs Hext changed between the first letter and the second?",
             "opts": ["She has become warmer and friendlier.",
                      "She has become stricter and colder.",
                      "She has stopped asking the boys to help.",
                      "She has started to smile at the cows."],
             "why": "At first she “does not smile much”; by February she smiles more, lets Arthur help with a pie and praises his pastry."},
            {"id": "5f18aaed7872", "t": "order", "d": "sequence", "q": "Put these events from the first letter in the order they happened.",
             "items": ["A lady gave the children a paper bag of food.",
                       "The children were taken to a village hall.",
                       "Mrs Hext said she would take both boys.",
                       "Mrs Hext gave the boys hot cocoa."],
             "why": "The bag was given on the long train journey; after getting off they went to the hall, were chosen by Mrs Hext, and had cocoa before bed."},
        ],
    },
    {
        "key": "RD6.04",
        "year": 6,
        "strand": "Biography",
        "title": "Louis Braille",
        "nc": "Retrieve, record and present information; summarise the main ideas drawn from more than one paragraph",
        "text": (
            "Louis Braille was born in 1809 in Coupvray, a small village near Paris, in France. His father made "
            "harnesses and saddles for horses, and his workshop was full of sharp tools. When Louis was three, he "
            "picked up one of these tools while playing, and it slipped and injured one of his eyes. An infection "
            "set in and spread to his other eye. By the age of five, Louis was completely blind.\n\n"
            "His family were determined that he should still learn. He went to the village school with the other "
            "children and listened carefully, and he did well. Then, when he was ten, he won a place at a special "
            "school for blind children in Paris.\n\n"
            "The school owned a few books for blind readers, but they were very hard to use. Each letter was a "
            "large raised shape pressed into thick paper, so a single book was enormous and heavy. Reading meant "
            "tracing every letter slowly with the fingers, and the pupils could not write anything in this way "
            "themselves.\n\n"
            "When Louis was about twelve, a former army captain named Charles Barbier visited the school. He had "
            "invented a system he called night writing, which used patterns of raised dots so that soldiers could "
            "read messages in the dark without lighting a lamp. The pupils were excited, but the system was "
            "difficult: it stood for sounds rather than letters, and one sign could need so many dots that it was "
            "too big to feel with one touch of a fingertip.\n\n"
            "Louis saw that the idea was a good one, even if the system was not. For the next three years he "
            "worked on it in every spare moment. By the age of fifteen he had found the answer: a small cell of "
            "just six dots, arranged in two columns of three. Each letter was a different pattern of dots, and "
            "every pattern fitted under a single fingertip. Readers could now move quickly along a line, and, just "
            "as importantly, blind people could write.\n\n"
            "Louis later became a teacher at the school, and he developed his code for numbers and music too. "
            "Sadly, he suffered from poor health for much of his life, and he died in 1852 at the age of only "
            "forty-three. Two years after his death, the school officially adopted his system.\n\n"
            "Today braille is used all over the world, in books, on signs and even on medicine boxes. The boy who "
            "lost his sight in his father's workshop gave millions of people the chance to read and write for "
            "themselves."
        ),
        "qs": [
            {"id": "44ff8d15283e", "t": "mcq", "d": "retrieve", "q": "According to the text, how did Louis lose his sight?",
             "opts": ["A tool he was playing with injured his eye, and an infection spread.",
                      "He was born blind in the village of Coupvray.",
                      "He read in the dark at night until his eyes failed.",
                      "A horse in his father's workshop kicked him in the face."],
             "why": "The first paragraph says a tool slipped and injured one eye, and an infection spread to the other."},
            {"id": "d69767f55fd6", "t": "mcq", "d": "infer", "q": "What does the second paragraph suggest about Louis as a young child?",
             "opts": ["He was clever and keen to learn, even though he could not see.",
                      "He did not enjoy school and wanted to work in the workshop.",
                      "He found it hard to keep up with the other children.",
                      "He was sent away to Paris because the village school refused him."],
             "no": {"He found it hard to keep up with the other children.": "The text says he listened carefully and did well."},
             "why": "He went to the ordinary village school, listened carefully, did well and then won a place at a school in Paris."},
            {"id": "cbaf945db72c", "t": "text", "d": "retrieve", "q": "Find and copy the name Charles Barbier gave to his system of raised dots.",
             "a": ["night writing", "night-writing"],
             "why": "The fourth paragraph says he had invented a system he called night writing, for soldiers reading in the dark."},
            {"id": "0797c27d29d6", "t": "mcq", "d": "compare", "q": "Using information from the text, what was one advantage of Louis's system over Barbier's?",
             "opts": ["Every sign could be felt with one touch of a fingertip.",
                      "It used patterns of raised dots instead of raised letters.",
                      "It could be read in the dark without lighting a lamp.",
                      "It stood for sounds rather than for letters."],
             "no": {"It used patterns of raised dots instead of raised letters.": "Barbier's night writing used raised dots too.",
                    "It stood for sounds rather than for letters.": "That was Barbier's system; in Louis's, each letter was a pattern of dots."},
             "why": "Barbier's signs could be too big to feel with one fingertip; in Louis's six-dot cell, every pattern fitted under a single fingertip."},
            {"id": "0be3b801a526", "t": "tap", "d": "vocab", "q": "Tap the word in this sentence that means “took up and began to use”.",
             "s": "Two years after his death, the school officially [adopted] his system.",
             "why": "To adopt a system is to take it up and start using it: the school began to use braille in 1854."},
            {"id": "6186b36cdffd", "t": "order", "d": "sequence", "q": "Put these events from Louis Braille's life in order.",
             "items": ["Louis became blind.",
                       "Louis went to a school for blind children in Paris.",
                       "Charles Barbier visited the school.",
                       "Louis invented his six-dot code.",
                       "The school officially adopted his system."],
             "why": "He was blind by five, went to Paris at ten, met Barbier at about twelve, had his code by fifteen, and the school adopted it two years after his death."},
            {"id": "31db49df9729", "t": "mcq", "d": "summarise", "q": "Which of these would be the best summary of the whole text?",
             "opts": ["A blind boy improved an idea he was shown and gave blind people a way to read and write.",
                      "An army captain invented a way for soldiers to read messages in the dark.",
                      "A school in Paris owned some huge, heavy books that were hard to read.",
                      "A boy was injured in his father's workshop and had to leave his village."],
             "why": "Barbier, the heavy books and the accident are each one part of the story; the text as a whole is about how Louis created braille and what it gave the world."},
        ],
    },
    {
        "key": "RD6.05",
        "year": 6,
        "strand": "Explanations",
        "title": "How do we see?",
        "nc": "Retrieve and record information from non-fiction; summarise the main ideas drawn from more than one paragraph",
        "text": (
            "Close your eyes and the world disappears. Open them and it rushes back: the colours of your bedroom, "
            "the words on this page, the face of a friend. But what actually happens when you see something? The "
            "answer is all about light.\n\n"
            "Light comes from light sources. The Sun is our most important one, but lamps, torches, candles and "
            "screens are light sources too: they give out their own light. Most of the things around you, such as "
            "a chair, a book or a tree, are not light sources at all. You can see them only because light from a "
            "source bounces off them. This bouncing is called reflection.\n\n"
            "Here is the key idea: light travels in straight lines. When light from the Sun hits an apple, some of "
            "it reflects off the apple's skin. A little of that reflected light travels in a straight line into "
            "your eye. Your eye detects it and sends a message to your brain, and your brain works out that you are "
            "looking at an apple. So you do not see an object by sending something out from your eyes, as some "
            "thinkers in ancient Greece believed. You see it because light enters your eyes.\n\n"
            "This explains why you cannot see anything in a completely dark room. With no light source, there is "
            "no light to reflect off the objects, so nothing can travel into your eyes. It is not that your eyes "
            "stop working: there is simply nothing for them to detect.\n\n"
            "Straight-line travel also explains shadows. When an object that light cannot pass through blocks the "
            "light from a source, a dark area forms behind it, where the light cannot reach. Because the light "
            "cannot bend around the object, the shadow has the same outline shape as the object itself.\n\n"
            "Some surfaces reflect light better than others. Smooth, shiny surfaces, such as mirrors, reflect light "
            "neatly, which is why you can see a clear image in them. A periscope uses two mirrors to bounce light "
            "around corners, so that a person can see over a wall, or out of a submarine, while staying hidden.\n\n"
            "Next time you look at anything at all, remember the journey that light has made: from a light source, "
            "off the object, and in a straight line into your eye."
        ),
        "qs": [
            {"id": "05c0d8d518de", "t": "mcq", "d": "retrieve", "q": "Which of these is a light source, according to the text?",
             "opts": ["a torch", "a mirror", "an apple", "a book"],
             "why": "The second paragraph lists lamps, torches, candles and screens as light sources. A mirror only reflects light; it gives out none of its own."},
            {"id": "c0434b3529d5", "t": "tap", "d": "vocab", "q": "Tap the word that means “notices” or “senses”.",
             "s": "Your eye [detects] it and sends a message to your brain, and your brain works out that you are looking at an apple.",
             "why": "To detect something is to notice or sense it: the eye senses the light that reaches it."},
            {"id": "0d266d075a98", "t": "order", "d": "sequence", "q": "Put these steps in the order they happen when you see an apple.",
             "items": ["Light comes from the Sun.",
                       "Light reflects off the apple's skin.",
                       "Reflected light travels into your eye.",
                       "Your eye sends a message to your brain."],
             "why": "The third paragraph follows the light: from the Sun, off the apple, in a straight line into the eye, then a message to the brain."},
            {"id": "45bc653b4958", "t": "mcq", "d": "retrieve", "q": "Using information from the text, why can you not see in a completely dark room?",
             "opts": ["There is no light to reflect off the objects.",
                      "Your eyes stop working when it is dark.",
                      "The objects give out less light at night.",
                      "The light bends around the objects."],
             "why": "The fourth paragraph says that with no light source there is no light to reflect into your eyes; your eyes still work."},
            {"id": "6cd1c43b4fe1", "t": "mcq", "d": "infer", "q": "Zainab holds a star-shaped card between a torch and a wall. Using the text, what shape will its shadow be?",
             "opts": ["a star", "a circle, like the torch", "a square, like the wall", "a blurred shape with no outline"],
             "why": "Light cannot bend around the card, so the shadow has the same outline shape as the object: a star."},
            {"id": "08fbcb193239", "t": "mcq", "d": "structure", "q": "Why does the writer begin with “Close your eyes and the world disappears”?",
             "opts": ["to hook the reader with something they can try for themselves",
                      "to explain how a periscope is able to see around corners",
                      "to give the scientific meaning of the word reflection",
                      "to warn readers not to look straight at the Sun"],
             "why": "The opening asks the reader to try something simple, which makes them curious about the question that follows: what happens when we see?"},
            {"id": "33cd0e25c71a", "t": "mcq", "d": "summarise", "q": "Which sentence best sums up the main idea of the whole text?",
             "opts": ["We see things because light from them travels into our eyes.",
                      "Shadows have the same outline shape as the objects that make them.",
                      "Mirrors are the best surfaces for reflecting light neatly.",
                      "The Sun is the most important light source that we have."],
             "why": "Every paragraph builds up to the journey in the last sentence: light from a source, off the object, into your eye. The others are details."},
        ],
    },
    {
        "key": "RD6.06",
        "year": 6,
        "strand": "Stories",
        "title": "The noise in the loft",
        "nc": "Discuss and evaluate how authors use language, including figurative language, considering the impact on the reader",
        "text": (
            "The storm reached the cottage just after nine. First the wind began to moan in the chimney, then the "
            "rain arrived, flung against the windows in handfuls. At half past nine, with a soft click, every "
            "light went out.\n\n"
            "“Power cut,” said Ife firmly, because one of them had to sound calm. Her little brother, Tobi, had "
            "already pulled the blanket up to his nose. Dad had driven to the village for milk twenty minutes "
            "earlier, and now the only sound was the storm.\n\n"
            "Ife found the torch in the kitchen drawer, exactly where Dad had said it would be. Its beam was thin "
            "and yellow, and it made the shadows in the corners lean and stretch. She was halfway back to the sofa "
            "when she heard it.\n\n"
            "Scratch. Scratch. Then a pause, long enough for her to wonder whether she had imagined it. Scratch.\n\n"
            "It was coming from above them, from the loft.\n\n"
            "“Ife,” Tobi whispered, “what is that?”\n\n"
            "“Mice,” she said, although no mouse she had ever heard made a sound that big.\n\n"
            "Then came a noise that froze her to the spot: a long, rasping shriek that seemed to tear through the "
            "ceiling. Tobi squeaked and vanished completely under the blanket.\n\n"
            "Ife's heart was hammering. Every part of her wanted to dive under the blanket too. Instead, she made "
            "herself think. The cottage was old, there were fields all around, and Dad had said that the hatch to "
            "the loft had been broken for years. Whatever was up there had probably come in from outside.\n\n"
            "Slowly, she carried a chair to the landing, climbed onto it and pushed the hatch up a few "
            "centimetres. She raised the torch.\n\n"
            "Two enormous dark eyes stared back at her from a heart-shaped white face. For a long moment, neither "
            "of them moved. Then the bird ruffled its pale feathers and gave a furious hiss.\n\n"
            "“Tobi!” she called, her voice wobbling with relief and laughter. “It's an owl. A barn owl. I think "
            "she's got a nest up here.”\n\n"
            "When Dad came in, dripping, ten minutes later, he found both children sitting on the landing in the "
            "dark, talking in whispers about whether the owl had chicks, and what she might be catching in the wet "
            "fields.\n\n"
            "“Well,” he said, “I see you've met our lodger.”"
        ),
        "qs": [
            {"id": "710f1f55e531", "t": "mcq", "d": "language", "q": "“The rain arrived, flung against the windows in handfuls.” What does this phrase suggest about the rain?",
             "opts": ["It was heavy and hit the glass hard, as if thrown.",
                      "It was light and fell gently on the roof.",
                      "It had stopped before the lights went out.",
                      "It was being collected by someone outside."],
             "why": "To fling something is to throw it hard; “in handfuls” makes the rain sound like heavy bursts thrown at the windows."},
            {"id": "496512284dcf", "t": "mcq", "d": "structure", "q": "Why does the writer use very short sentences, such as “Scratch. Scratch.”, in the fourth paragraph?",
             "opts": ["to copy the sound and build suspense, as Ife listens",
                      "to show that Ife was too tired to think clearly",
                      "to make the paragraph quicker to read aloud",
                      "to show that the noise was coming from the kitchen"],
             "why": "Each “Scratch.” stands alone like the sound itself, and the pause between them makes the reader wait and listen with Ife."},
            {"id": "bfd493f98423", "t": "mcq", "d": "infer", "q": "“Mice,” she said, although no mouse she had ever heard made a sound that big. What does this show about Ife?",
             "opts": ["She did not really believe it was mice but wanted to calm Tobi.",
                      "She was sure that the noise was being made by mice.",
                      "She had seen mice in the loft earlier that day.",
                      "She wanted to frighten Tobi with a story about mice."],
             "why": "She knows mice do not make a sound that big, yet she says it anyway, just as she tried to “sound calm” about the power cut for her brother."},
            {"id": "72270b03d21e", "t": "tap", "d": "infer", "q": "Tap the word that shows Ife was very frightened.",
             "s": "Ife's heart was [hammering].",
             "why": "A hammering heart is beating very hard and fast, which is what happens when someone is frightened."},
            {"id": "0d35126e4cce", "t": "mcq", "d": "retrieve", "q": "Which clue helped Ife work out that the creature had come in from outside?",
             "opts": ["The hatch to the loft had been broken for years.",
                      "Dad had left the back door of the cottage open.",
                      "She had heard footsteps going across the kitchen.",
                      "Tobi had seen something moving past the window."],
             "why": "She remembered that the cottage was old, had fields all around, and that the loft hatch had been broken for years."},
            {"id": "27a24de35cdb", "t": "mcq", "d": "vocab", "q": "Dad says, “I see you've met our lodger.” Which is closest in meaning to lodger?",
             "opts": ["someone who lives in another person's home",
                      "someone who mends broken roofs and hatches",
                      "a visitor who comes only for one evening",
                      "a pet that has been trained to guard a house"],
             "why": "A lodger lives in a house that belongs to someone else. Dad jokes that the owl is living in their loft."},
            {"id": "47e45bd209f9", "t": "order", "d": "sequence", "q": "Put these events in the order they happen in the story.",
             "items": ["Every light in the cottage went out.",
                       "Ife found the torch in the kitchen drawer.",
                       "A rasping shriek came from the loft.",
                       "Ife lifted the hatch and saw the owl.",
                       "Dad came back from the village."],
             "why": "The power cut came first; Ife fetched the torch, heard the scratching and the shriek, looked in the loft, and Dad arrived ten minutes later."},
        ],
    },
    {
        "key": "RD6.07",
        "year": 6,
        "strand": "Information",
        "title": "The Maya: cities and numbers",
        "nc": "Distinguish between statements of fact and opinion; retrieve and record information from non-fiction",
        "text": (
            "More than a thousand years ago, in the rainforests and lowlands of what are now southern Mexico, "
            "Guatemala, Belize and Honduras, the Maya built a remarkable civilisation. Its greatest period, which "
            "historians call the Classic period, lasted from about AD 250 to AD 900. During that time the Maya "
            "built dozens of cities, linked by trade routes and raised stone roads.\n\n"
            "Maya cities were not like modern ones. At the centre stood great plazas, stone palaces and tall "
            "stepped pyramids made from blocks of limestone, often painted bright red. Around them spread houses "
            "with thatched roofs, gardens and fields. Tikal, in the rainforest of Guatemala, was one of the largest "
            "cities, and its pyramids still rise above the treetops today. Most cities also had a ball court, a "
            "long stone alley where players kept a heavy rubber ball moving using their hips.\n\n"
            "The Maya were skilled farmers. Their most important crop was maize, which they ground up and cooked "
            "in many ways, such as in a thick porridge. They also grew beans, squash, chilli peppers and cacao, whose beans were so "
            "valuable that they were sometimes used as money.\n\n"
            "Perhaps the most impressive Maya achievement was their number system. While we count in tens, the "
            "Maya counted in twenties, possibly because people have twenty fingers and toes. They wrote numbers "
            "using just three symbols: a dot for one, a bar for five, and a shape like a shell for zero. So seven "
            "was written as one bar with two dots above it, and nineteen as three bars with four dots above "
            "them.\n\n"
            "For numbers of twenty and above, the Maya stacked their symbols in levels, reading from the bottom "
            "up. The bottom level showed ones, and the level above it showed twenties. Twenty itself was written "
            "as a single dot on the upper level with a shell on the bottom level, meaning one twenty and no ones. "
            "Using a symbol for zero in this way was a huge step: the Romans, for example, had no zero at all.\n\n"
            "The Maya used their numbers to keep careful records, to trade and to follow the movements of the Sun, "
            "the Moon and the planets, which helped them to make a very accurate calendar. They also developed a "
            "writing system of picture-like signs called glyphs, which they carved into stone and painted in "
            "folding books.\n\n"
            "Around AD 900, many of the great southern cities were abandoned. Nobody is completely sure why, "
            "although long droughts may have played a part. But the Maya did not disappear. Millions of Maya "
            "people still live in Central America today, and many still speak Mayan languages."
        ),
        "qs": [
            {"id": "ca4d08cfc873", "t": "text", "d": "retrieve", "q": "Find and copy the name of one of the largest Maya cities.",
             "a": ["Tikal"],
             "why": "The second paragraph says Tikal, in the rainforest of Guatemala, was one of the largest cities."},
            {"id": "bd2730dedfc3", "t": "mcq", "d": "retrieve", "q": "According to the text, what were cacao beans sometimes used as?",
             "opts": ["money", "thatch for roofs","balls for the ball court", "paint for the pyramids"],
             "why": "The third paragraph says cacao beans were so valuable that they were sometimes used as money."},
            {"id": "720e548f5e3c", "t": "mcq", "d": "compare", "q": "How was the Maya way of counting different from ours?",
             "opts": ["They counted in twenties; we count in tens.",
                      "They counted in fives; we count in twenties.",
                      "They had no zero; we have a symbol for zero.",
                      "They read numbers from the top level down."],
             "why": "The fourth paragraph says we count in tens while the Maya counted in twenties. They did have a zero, and they read from the bottom up."},
            {"id": "d9314e642d2b", "t": "mcq", "d": "infer", "q": "Using information from the text, how would the Maya have written the number twelve?",
             "opts": ["two bars with two dots above them",
                      "one bar with two dots above it",
                      "twelve dots in a single row",
                      "one dot above a shell"],
             "why": "A bar is five and a dot is one, so twelve is two bars (ten) and two dots. One bar and two dots is seven; a dot above a shell is twenty."},
            {"id": "68761fb4466b", "t": "tap", "d": "retrieve", "q": "Tap the word that names the picture-like signs the Maya used for writing.",
             "s": "They also developed a writing system of picture-like signs called [glyphs], which they carved into stone and painted in folding books.",
             "why": "The sixth paragraph says the signs were called glyphs."},
            {"id": "9fc207158ec2", "t": "mcq", "d": "vocab", "q": "“Many of the great southern cities were abandoned.” Which is closest in meaning to abandoned?",
             "opts": ["left empty by the people who lived there",
                      "knocked down and rebuilt in a new style",
                      "buried deep under the rainforest floor",
                      "joined together by new stone roads"],
             "why": "Abandoned means left behind: the people moved away, but the Maya themselves did not disappear."},
            {"id": "be4065f5e4b7", "t": "mcq", "d": "purpose", "q": "Which of these is an opinion, not a fact?",
             "opts": ["Perhaps the most impressive Maya achievement was their number system.",
                      "The Maya wrote numbers using a dot, a bar and a shell shape.",
                      "Tikal is in the rainforest of Guatemala.",
                      "The Maya grew maize, beans and squash."],
             "why": "Whether something is “the most impressive” is a judgement that people could disagree about, and “perhaps” shows it is the writer's view. The others can be checked."},
        ],
    },
    {
        "key": "RD6.08",
        "year": 6,
        "strand": "Persuasive writing",
        "title": "Should pupils wear school uniform?",
        "nc": "Identify how language, structure and presentation contribute to meaning; distinguish arguments for and against",
        "text": (
            "Most secondary schools in the United Kingdom, and many primary schools, ask their pupils to wear a "
            "uniform. Some people think this is a sensible tradition; others think it is out of date. So should "
            "pupils have to wear school uniform? There are strong arguments on both sides.\n\n"
            "Supporters of uniform say that it creates a sense of belonging. When everyone wears the same colours "
            "and badge, pupils can feel part of one community, and they may feel proud to represent their school "
            "on trips and at sports matches. Uniform also makes pupils easy to spot, which can help teachers keep "
            "everyone safe on a crowded visit to a museum or a beach.\n\n"
            "Another argument for uniform is that it reduces pressure. Without a uniform, some children might feel "
            "they have to wear expensive, fashionable clothes every day, and those who cannot afford them could be "
            "teased. A uniform, supporters argue, puts everyone on a level playing field. Many parents also like "
            "the fact that there is no argument every morning about what to wear.\n\n"
            "On the other hand, critics point out that uniform can be costly. Blazers, ties and jumpers with the "
            "school badge sewn on often have to be bought from one particular shop, and they can cost far more "
            "than ordinary clothes. For families with several children, this can be a real burden, especially when "
            "children grow quickly.\n\n"
            "Critics also argue that uniform stops young people from expressing who they are. Choosing what to "
            "wear is one way that people show their personality, and some believe that schools should encourage "
            "this rather than prevent it. Others say that stiff collars and ties are simply uncomfortable, and that "
            "pupils learn best when they are comfortable.\n\n"
            "Some schools have found a middle way. They keep a uniform but make it simpler and cheaper: for "
            "example, a plain sweatshirt that can be bought in many shops, with a badge that can be ironed on at "
            "home. Others hold occasional non-uniform days, when pupils can wear their own clothes.\n\n"
            "In conclusion, there are good reasons both for and against school uniform. It can bring pupils "
            "together and reduce pressure, but it can also be expensive and uncomfortable. Perhaps the best answer "
            "is a uniform that is simple, affordable and comfortable, so that schools gain the benefits without the "
            "drawbacks. What do you think?"
        ),
        "qs": [
            {"id": "cedb7e7d952a", "t": "mcq", "d": "retrieve", "q": "According to the text, how can uniform help teachers on a school trip?",
             "opts": ["It makes pupils easy to spot in a crowd.",
                      "It makes pupils behave better in museums.",
                      "It makes the trip cheaper for families.",
                      "It stops pupils arguing about what to wear."],
             "why": "The second paragraph says uniform makes pupils easy to spot, which helps teachers keep everyone safe on a crowded visit."},
            {"id": "c8f8841db58c", "t": "mcq", "d": "vocab", "q": "“A uniform, supporters argue, puts everyone on a level playing field.” What does “on a level playing field” mean here?",
             "opts": ["on equal terms, with no one at a disadvantage",
                      "outside on the school sports field",
                      "in a straight line, ready for a race",
                      "dressed for games lessons and matches"],
             "why": "A level field is fair to both teams. In uniform, no child stands out for having cheaper or less fashionable clothes, so everyone is equal."},
            {"id": "74cec9b6cb10", "t": "tap", "d": "vocab", "q": "Tap the word that means “a heavy load or difficulty”.",
             "s": "For families with several children, this can be a real [burden], especially when children grow quickly.",
             "why": "A burden is something heavy to carry; here it means a cost that is hard for families to manage."},
            {"id": "c53598dad7c4", "t": "mcq", "d": "infer", "q": "Using the text, why might a parent with four children be against school uniform?",
             "opts": ["Buying it from one shop for growing children costs a lot.",
                      "The children would be teased for wearing uniform.",
                      "The children would be too easy to spot on trips.",
                      "Non-uniform days happen too often at most schools."],
             "why": "The fourth paragraph says uniform often comes from one shop, costs more than ordinary clothes and is a burden for families with several children who grow quickly."},
            {"id": "ea42f0fe54d8", "t": "mcq", "d": "structure", "q": "Why does the writer begin the fourth paragraph with “On the other hand”?",
             "opts": ["to show the text is turning from arguments for uniform to arguments against",
                      "to give one more reason why uniform creates a sense of belonging",
                      "to show that the writer is about to give the final conclusion",
                      "to introduce a list of the shops that sell school uniform"],
             "why": "“On the other hand” signals the other side of an argument: the paragraphs before it are for uniform, the ones after it are against."},
            {"id": "7929a0c33c92", "t": "mcq", "d": "compare", "q": "How are the schools that have found “a middle way” different from schools with a traditional uniform?",
             "opts": ["Their uniform is simpler and cheaper to buy.",
                      "They have no uniform for pupils at all.",
                      "Their pupils wear blazers only on trips.",
                      "Their pupils may choose their own badge."],
             "why": "The sixth paragraph says these schools keep a uniform but make it simpler and cheaper, such as a plain sweatshirt with an iron-on badge."},
            {"id": "3cd54927e444", "t": "mcq", "d": "purpose", "q": "What is the main purpose of this text?",
             "opts": ["to set out both sides of the argument before giving a view",
                      "to persuade readers that all schools should scrap uniform",
                      "to explain how school uniforms are designed and made",
                      "to advertise a shop that sells cheaper school uniform"],
             "why": "It is a balanced argument: it gives reasons for, then reasons against, and only then suggests a conclusion and asks the reader's view."},
        ],
    },
    {
        "key": "RD6.09",
        "year": 6,
        "strand": "Explanations",
        "title": "Changing a circuit",
        "nc": "Explain and discuss understanding of what has been read; predict what might happen from details stated",
        "text": (
            "Every time you press a light switch or turn on a torch, you are using an electrical circuit. A circuit "
            "is a complete loop that electricity can flow around. If there is a gap anywhere in the loop, the "
            "electricity stops flowing and nothing works.\n\n"
            "A simple circuit needs a few basic parts. A cell, often called a battery, pushes the electricity "
            "around. Wires, usually made of copper covered in plastic, carry it. Copper is a good conductor, which "
            "means that electricity flows through it easily; the plastic coating is an insulator, which stops the "
            "electricity from escaping and protects anyone who touches the wire. Finally, a component such as a "
            "bulb, a buzzer or a motor uses the electricity to do something useful.\n\n"
            "Scientists and engineers draw circuits using symbols instead of pictures. A cell is shown as a long "
            "line and a short line side by side. A bulb is a circle with a cross inside it. An open switch is drawn "
            "as a short line raised at an angle, like a drawbridge. Because everyone uses the same symbols, a "
            "circuit diagram drawn in Manchester can be understood in Mumbai.\n\n"
            "A switch is simply a way of closing or opening the gap. When a switch is closed, the loop is complete "
            "and the bulb lights. When it is open, there is a gap and the bulb goes out.\n\n"
            "What happens if you change the circuit? Suppose you start with one cell and one bulb. If you add a "
            "second cell, facing the same way as the first, the bulb glows more brightly, because there is a "
            "greater push, called the voltage. The voltage of a cell is printed on its side and measured in volts; "
            "a typical torch cell is 1.5 volts. In the same way, adding a cell to a circuit with a buzzer makes the "
            "buzzer louder.\n\n"
            "Now suppose you keep one cell but add a second bulb into the same loop. This time, both bulbs glow "
            "more dimly than the single bulb did, because the push from the cell is shared between them. Add a "
            "third bulb and they will all be dimmer still.\n\n"
            "Be careful, though. Too many cells for one small bulb can make it burn out, and a broken bulb leaves a "
            "gap in the circuit. Electricity from the mains sockets in your home is far more powerful than any "
            "battery and can cause serious injuries, so you should never experiment with it. Batteries are for "
            "experiments; sockets are not."
        ),
        "qs": [
            {"id": "4acb31dc3543", "t": "mcq", "d": "retrieve", "q": "According to the text, why are copper wires covered in plastic?",
             "opts": ["Plastic is an insulator, so it stops electricity escaping.",
                      "Plastic is a good conductor, so it carries the electricity.",
                      "Plastic makes the bulbs in the circuit glow more brightly.",
                      "Plastic pushes the electricity around the whole loop."],
             "why": "The second paragraph says the plastic coating is an insulator, which stops electricity escaping and protects anyone who touches the wire."},
            {"id": "ceb346ed95a4", "t": "text", "d": "vocab", "q": "Find and copy one word from the second paragraph that means a material electricity flows through easily.",
             "a": ["conductor", "a conductor", "good conductor", "a good conductor", "conductors", "good conductors"],
             "why": "The text says copper is a good conductor, which means that electricity flows through it easily.",
             "no": {"insulator": "An insulator does the opposite: it stops electricity from flowing through it."}},
            {"id": "10f6d82631eb", "t": "mcq", "d": "language", "q": "The writer says the open switch symbol looks “like a drawbridge”. Why is this comparison helpful?",
             "opts": ["It helps the reader picture a line lifted up to leave a gap.",
                      "It shows that switches were first used in castles.",
                      "It tells the reader that switches are very heavy.",
                      "It explains why a bulb is drawn as a circle."],
             "why": "A raised drawbridge leaves a gap that nothing can cross, just as an open switch leaves a gap in the circuit."},
            {"id": "b662e3940923", "t": "mcq", "d": "infer", "q": "Why does the writer mention Manchester and Mumbai?",
             "opts": ["to show that circuit symbols are understood all over the world",
                      "to show that the best circuits are designed in those two cities",
                      "to explain that the two cities use different kinds of switch",
                      "to tell the reader where the first electrical circuits were made"],
             "why": "Two cities far apart are given as examples: because everyone uses the same symbols, a diagram from one can be read in the other."},
            {"id": "d062d5def6a5", "t": "tap", "d": "retrieve", "q": "Tap the scientific word for the push that the cells give.",
             "s": "If you add a second cell, facing the same way as the first, the bulb glows more brightly, because there is a greater push, called the [voltage].",
             "why": "The fifth paragraph says the greater push is called the voltage, measured in volts."},
            {"id": "621790a296ae", "t": "mcq", "d": "predict", "q": "Kofi's circuit has one cell and two bulbs. He adds a third bulb to the same loop. Using the text, what will happen?",
             "opts": ["All three bulbs will glow more dimly.",
                      "All three bulbs will glow more brightly.",
                      "Only the new bulb will light up.",
                      "The bulbs will stay exactly as bright."],
             "why": "The sixth paragraph says the cell's push is shared between the bulbs, so adding another bulb makes them all dimmer still."},
            {"id": "c9f61f6b56d1", "t": "mcq", "d": "structure", "q": "Why has the writer included the last paragraph?",
             "opts": ["to warn readers about the dangers of electricity",
                      "to explain how to make a bulb glow more brightly",
                      "to describe how circuit symbols are drawn",
                      "to persuade readers to buy more batteries"],
             "why": "The paragraph begins “Be careful, though” and warns about bulbs burning out and about mains sockets, which can cause serious injuries."},
        ],
    },
    {
        "key": "RD6.10",
        "year": 6,
        "strand": "Stories",
        "title": "Page forty-two",
        "nc": "Draw inferences such as inferring characters' feelings, thoughts and motives from their actions",
        "text": (
            "Noor read the poem three times before she was sure. It was on page forty-two of a battered book of "
            "poems that her grandmother had given her years ago: a poem about a lighthouse in winter. It was also, "
            "word for word, the poem that her best friend, Ellie, had read out in assembly that morning as the "
            "winner of the Year 6 poetry competition. Everyone had clapped, and Ellie had gone pink and beamed as "
            "Mrs Okafor handed her the prize: a book token and a shiny certificate.\n\n"
            "Noor's own poem, the one she had worked on for two weeks, had come second.\n\n"
            "She closed the book and sat on her bed, feeling slightly sick. Part of her wanted to march into school "
            "the next morning and show Mrs Okafor the page. It was not fair. Copying was cheating. But another part "
            "of her remembered Ellie's face in assembly, how proud she had looked, how her little brother had "
            "cheered from the front row. If Noor told, everyone would know. Ellie might never speak to her "
            "again.\n\n"
            "And there was a third, smaller voice, one that Noor did not like very much. If she told, she might "
            "win instead. Was that the real reason she wanted to tell?\n\n"
            "She thought about it all evening. At dinner, her dad asked why she was pushing her rice around the "
            "plate, and she said she wasn't hungry. At bedtime, she was no closer to an answer.\n\n"
            "In the morning, she slipped the battered book into her bag. At the school gate, Ellie ran up to her, "
            "smiling, and then stopped. She must have seen something in Noor's face.\n\n"
            "“What's wrong?” Ellie asked.\n\n"
            "Noor took a breath. “I think you know,” she said quietly, and showed her the page.\n\n"
            "For a long moment, Ellie said nothing. Her smile crumpled. “I didn't think anyone would know it,” she "
            "whispered. “I couldn't think of anything good, and everyone else's were so clever, and I just...” She "
            "stopped. “Are you going to tell?”\n\n"
            "“No,” said Noor. “I think you should.”\n\n"
            "Ellie stared at the book. Then she nodded slowly, wiped her eyes on her sleeve, and turned towards the "
            "school office, where Mrs Okafor was talking to the secretary. Noor watched her go. She did not feel "
            "like a winner. But she felt, for the first time since yesterday, that she could breathe."
        ),
        "qs": [
            {"id": "1e0383118e47", "t": "mcq", "d": "retrieve", "q": "What prize did Ellie receive in assembly?",
             "opts": ["a book token and a certificate",
                      "a book of poems and a certificate",
                      "a trophy and a book token",
                      "a shiny medal and a certificate"],
             "why": "The first paragraph says Mrs Okafor handed her a book token and a shiny certificate. The book of poems belonged to Noor."},
            {"id": "4d2ccef54967", "t": "mcq", "d": "vocab", "q": "“A battered book of poems.” Which word is closest in meaning to battered?",
             "opts": ["worn and damaged", "brand new", "thick and heavy", "borrowed"],
             "why": "Battered means worn and damaged by a lot of use; Noor had been given the book years ago."},
            {"id": "5734dfad8e4b", "t": "mcq", "d": "infer", "q": "What is the “third, smaller voice” that Noor does not like?",
             "opts": ["the thought that telling might win her the prize",
                      "the worry that Ellie's brother would be upset",
                      "the feeling that copying was not really cheating",
                      "the fear that Mrs Okafor would not believe her"],
             "why": "The voice says that if she told, she might win instead. Noor does not like it because it would make telling selfish."},
            {"id": "484b2c6b4a8f", "t": "mcq", "d": "infer", "q": "Why was Noor pushing her rice around her plate at dinner?",
             "opts": ["She was too worried about what to do to feel like eating.",
                      "She had eaten a large lunch at school that day.",
                      "She was angry with her dad for asking questions.",
                      "She did not like the rice her dad had cooked."],
             "why": "She had thought about the problem all evening and felt slightly sick: worry had taken away her appetite."},
            {"id": "bc8096cce85e", "t": "tap", "d": "language", "q": "Tap the word that shows Ellie's happiness suddenly disappeared.",
             "s": "Her smile [crumpled].",
             "why": "Something that crumples collapses and folds in on itself; her smile fell apart when she saw the page."},
            {"id": "c36d5efeeaa9", "t": "mcq", "d": "predict", "q": "Using the ending, what is Ellie most likely to do next?",
             "opts": ["tell Mrs Okafor that the poem was not her own",
                      "ask Noor to hide the book of poems at home",
                      "read the lighthouse poem out in another assembly",
                      "stop speaking to Noor for the rest of the year"],
             "why": "Noor says Ellie should tell; Ellie nods and walks towards the office, where Mrs Okafor is."},
            {"id": "0f522ce7cb58", "t": "mcq", "d": "summarise", "q": "Which of these best describes the main theme of the story?",
             "opts": ["doing the right thing even when it is hard",
                      "working hard to win a writing competition",
                      "learning to write poems about the sea",
                      "a grandmother's gift to her granddaughter"],
             "why": "The story is about Noor's difficult choice and how both girls end up being honest, even though it hurts."},
        ],
    },
    {
        "key": "RD6.11",
        "year": 6,
        "strand": "Poems",
        "title": "The heron at Lock Seven",
        "nc": "Discuss and evaluate how authors use language, including figurative language, considering the impact on the reader",
        "text": (
            "Down where the canal goes quiet and green,\n"
            "past the lock gates, black and slick with rain,\n"
            "a heron stands in the shallows every morning,\n"
            "grey as the sky and as still as a post,\n"
            "while the joggers and cyclists hurry by\n"
            "and never see him at all.\n\n"
            "He has been there since before the mist lifted,\n"
            "one leg tucked away like a folded umbrella,\n"
            "his neck drawn down into his shoulders:\n"
            "an old man in a long grey coat\n"
            "waiting for a bus that never comes.\n\n"
            "But watch him. Watch his eye.\n"
            "It is yellow and bright as a bead of glass,\n"
            "and it does not blink.\n"
            "Beneath the water, where we see only brown,\n"
            "he sees the silver flicker of a fish.\n\n"
            "Slowly, slowly, the neck uncurls.\n"
            "Slowly, slowly, one foot lifts\n"
            "and settles again without a ripple,\n"
            "so carefully that the water hardly knows\n"
            "it has been touched.\n\n"
            "Then, faster than a breath, he strikes:\n"
            "a stab, a splash, a flash of silver,\n"
            "and the beak comes up, shining and full.\n"
            "One gulp, a shake of the head,\n"
            "and he is a post again,\n"
            "as if nothing had happened.\n\n"
            "I have stood on the towpath with my coat zipped up\n"
            "and my hands pushed deep in my pockets,\n"
            "counting the minutes he waits for one fish.\n"
            "Ten minutes. Twenty. Half an hour.\n"
            "I fidget after five.\n\n"
            "When at last he decides to leave,\n"
            "he does not hurry, even then.\n"
            "He opens those enormous wings like a creaking deckchair\n"
            "and pushes off from the water,\n"
            "legs trailing behind him like forgotten string,\n"
            "and rows slowly away over the rooftops.\n\n"
            "Tomorrow I will come back early,\n"
            "before the joggers and the bikes,\n"
            "and stand as still as I can manage\n"
            "on the wet stones by Lock Seven,\n"
            "to learn what the heron knows about waiting."
        ),
        "qs": [
            {"id": "e0d81aeb3405", "t": "mcq", "d": "language", "q": "In the second verse, the heron is “an old man in a long grey coat / waiting for a bus that never comes”. What does this suggest about the heron?",
             "opts": ["He stands hunched and patient, as if he could wait for ever.",
                      "He is too old and weak to catch fish any more.",
                      "He is cross because he has been kept waiting.",
                      "He is getting ready to fly off to somewhere new."],
             "why": "With his neck drawn into his shoulders he looks hunched like an old man, and someone waiting for a bus that never comes waits a very long time."},
            {"id": "6f84780ae14e", "t": "text", "d": "retrieve", "q": "Find and copy the word that tells you the colour of the heron's eye.",
             "a": ["yellow"],
             "why": "The third verse says his eye is yellow and bright as a bead of glass.",
             "no": {"grey": "Grey is the colour of the heron's body, “grey as the sky”, not his eye."}},
            {"id": "b92bd3b4d38b", "t": "mcq", "d": "structure", "q": "Why does the poet begin two lines of the fourth verse with “Slowly, slowly”?",
             "opts": ["to make the reader feel how carefully and gradually the heron moves",
                      "to show that the heron is tired after standing still all morning",
                      "to tell the reader that the fish is swimming slowly away",
                      "to show that the speaker is walking slowly along the towpath"],
             "why": "Repeating the words slows the reader down too, so the lines move as gently as the heron, who does not even make a ripple."},
            {"id": "ef2f36036429", "t": "tap", "d": "infer", "q": "Tap the word that shows the speaker finds it hard to keep still.",
             "s": "I [fidget] after five.",
             "why": "To fidget is to keep making small restless movements: the speaker cannot keep still for more than five minutes."},
            {"id": "1e834d5b734a", "t": "mcq", "d": "compare", "q": "How is the speaker different from the heron?",
             "opts": ["The speaker grows restless quickly, but the heron waits a long time.",
                      "The speaker hurries past, but the heron flies off quickly.",
                      "The speaker catches fish, but the heron only watches them.",
                      "The speaker comes at night, but the heron comes in the morning."],
             "why": "The heron waits half an hour for one fish, while the speaker fidgets after five minutes."},
            {"id": "aa8cb55839e9", "t": "mcq", "d": "vocab", "q": "“Legs trailing behind him like forgotten string.” Which is closest in meaning to trailing?",
             "opts": ["hanging loosely behind", "kicking very hard", "folded up tightly", "pointing straight up"],
             "why": "Trailing means being pulled along loosely behind, like a piece of string someone forgot to wind up."},
            {"id": "68512ec36c32", "t": "mcq", "d": "summarise", "q": "Which of these is the main idea of the poem?",
             "opts": ["Watching a patient heron teaches the speaker about waiting.",
                      "Herons are in danger because joggers disturb the canal.",
                      "The speaker wants to learn how to catch fish in a canal.",
                      "Canals are busy places full of joggers and cyclists."],
             "why": "The poem describes how still and patient the heron is, compares the restless speaker with it, and ends with the speaker wanting to learn what the heron knows about waiting."},
        ],
    },
    {
        "key": "RD6.12",
        "year": 6,
        "strand": "Information",
        "title": "Sorting the living world",
        "nc": "Retrieve, record and present information from non-fiction; explain and discuss understanding of what has been read",
        "text": (
            "Scientists have so far named well over a million different kinds of animal, and many more are still "
            "waiting to be discovered. With so many living things, how does anyone keep track? The answer is "
            "classification: sorting living things into groups according to the features they share.\n\n"
            "People have tried to sort living things for thousands of years, but the system we use today owes most "
            "to a Swedish scientist called Carl Linnaeus, who lived in the eighteenth century. Linnaeus gave every "
            "species a two-part name in Latin. The first part names the group it belongs to, and the second part "
            "names the species itself. Humans, for example, are Homo sapiens. This system means that a scientist "
            "in Japan and a scientist in Brazil know they are talking about exactly the same creature, even though "
            "its everyday names in Japanese and Portuguese are completely different.\n\n"
            "At the broadest level, living things are often sorted into large groups such as plants, animals and "
            "micro-organisms, which are living things so tiny that they can only be seen with a microscope. Each "
            "group is then divided again and again into smaller and smaller groups.\n\n"
            "Animals, for instance, can be split into two huge groups. Vertebrates are animals with a backbone. "
            "Invertebrates have no backbone; this group includes insects, spiders, worms, snails and jellyfish, and "
            "it is by far the larger of the two. Vertebrates are then divided into five groups: fish, amphibians, "
            "reptiles, birds and mammals.\n\n"
            "Classifying animals means looking carefully at their features, not at where they live or how they "
            "look at first glance. A whale lives in the sea and is shaped rather like a fish, yet it is a mammal: "
            "it breathes air with lungs, it is warm-blooded, and it feeds its young on milk. A bat flies like a "
            "bird, but it has fur rather than feathers and also feeds its young on milk, so it too is a mammal. A "
            "penguin cannot fly at all, but its feathers and beak make it a bird.\n\n"
            "To identify an unknown living thing, scientists often use a classification key. A key is a set of "
            "questions, each with only two possible answers, such as “Does it have legs?” or “Does it have more "
            "than six legs?” Each answer leads to another question, until only one possible group or species is "
            "left.\n\n"
            "Classification is not just a tidy way of making lists. It helps scientists to share what they know "
            "about each living thing, and it helps conservationists to know exactly which species need "
            "protecting."
        ),
        "qs": [
            {"id": "be12f3679c18", "t": "mcq", "d": "retrieve", "q": "According to the text, which country did Carl Linnaeus come from?",
             "opts": ["Sweden", "Japan", "Brazil", "Portugal"],
             "why": "The second paragraph calls him a Swedish scientist. Japan and Brazil are only examples of where scientists might work."},
            {"id": "4515964e3c07", "t": "mcq", "d": "infer", "q": "Why does the writer mention a scientist in Japan and a scientist in Brazil?",
             "opts": ["to show that Latin names let scientists everywhere agree on a species",
                      "to show that Linnaeus travelled to both countries to find animals",
                      "to explain that the two countries have the most kinds of animal",
                      "to suggest that scientists should all learn Japanese and Portuguese"],
             "why": "The everyday names differ from language to language, but the two-part Latin name is the same, so both scientists know they mean the same creature."},
            {"id": "ef95358d14ea", "t": "text", "d": "vocab", "q": "Find and copy the word that means living things so tiny they can only be seen with a microscope.",
             "a": ["micro-organisms", "microorganisms", "micro-organism", "microorganism", "the micro-organisms", "the microorganisms"],
             "why": "The third paragraph says micro-organisms are living things so tiny that they can only be seen with a microscope."},
            {"id": "e37c3ce10569", "t": "tap", "d": "retrieve", "q": "Tap the word that names the group of animals with no backbone.",
             "s": "[Invertebrates] have no backbone; this group includes insects, spiders, worms, snails and jellyfish, and it is by far the larger of the two.",
             "why": "Invertebrates have no backbone; vertebrates are the animals that do have one."},
            {"id": "ab319c9bb334", "t": "mcq", "d": "compare", "q": "Using information from the text, what do whales and bats have in common?",
             "opts": ["They both feed their young on milk.",
                      "They both live in the sea.",
                      "They both have feathers.",
                      "They both breathe with gills."],
             "why": "The fifth paragraph says a whale feeds its young on milk and a bat “also feeds its young on milk”: that is why both are mammals."},
            {"id": "e8b18ef594c9", "t": "mcq", "d": "infer", "q": "Why does the writer include the example of the penguin?",
             "opts": ["to show that an animal is grouped by its features, not by what it can do",
                      "to show that every bird that cannot fly is really a kind of mammal",
                      "to show that animals that live in the sea are all grouped as fish",
                      "to show that a classification key only works for animals that fly"],
             "why": "The paragraph begins by saying classifying means looking at features. A penguin cannot fly, yet its feathers and beak make it a bird."},
            {"id": "355ba623b070", "t": "mcq", "d": "purpose", "q": "What is the writer's main purpose in this text?",
             "opts": ["to explain how and why scientists sort living things into groups",
                      "to persuade readers to protect whales, bats and penguins",
                      "to tell the story of Carl Linnaeus's life from start to finish",
                      "to teach readers how to speak Latin like scientists"],
             "why": "Most of the text explains how living things are grouped, and the last paragraph explains why it matters. Linnaeus appears in one paragraph only."},
        ],
    },
    {
        "key": "RD6.13",
        "year": 6,
        "strand": "Stories",
        "title": "The final",
        "nc": "Identify how structure and presentation contribute to meaning; make comparisons within a book",
        "text": (
            "With two minutes left of the Under-12 County Cup final, the score was still 1-1, and Hodan's legs felt "
            "as if they were made of wet sand.\n\n"
            "She had run more in the last hour than in the whole season. The pitch at Riverside Park was heavy with "
            "rain, and every tackle sent up a spray of mud. Along the touchline, a long row of umbrellas bobbed and "
            "swayed, and somewhere among them was her grandad, who never missed a match and never stopped shouting "
            "“Go on, Hodan!” even when she was standing still.\n\n"
            "The other team, Ashford Rovers, had not lost a game all year. Their captain, a tall girl with a fierce "
            "ponytail, had scored in the first five minutes, and for a long time it had looked as if Hodan's team, "
            "Millbrook Juniors, would be swept away. But just before half-time, Hodan had sent a cross curling into "
            "the box, and Priya had headed it in. Since then, neither side had managed to break through.\n\n"
            "Now the ball broke loose near the halfway line. Hodan reached it first. In front of her there was "
            "space, a whole green stretch of it, and for once nobody was close enough to stop her. She ran. The "
            "Rovers defenders turned and chased. She could hear their boots slapping on the wet grass behind her, "
            "closer and closer.\n\n"
            "The goalkeeper came rushing out, arms wide, making herself enormous. Hodan had a choice. She could "
            "shoot from here, from a difficult angle, and perhaps become the girl who won the cup. Or she could pass "
            "to Grace, who was racing up on her left, completely unmarked, with an empty goal in front of her.\n\n"
            "Hodan had dreamed of scoring in a final ever since she was seven.\n\n"
            "She passed.\n\n"
            "Grace did not even have to kick it hard. The ball rolled gently over the line, and the whole of "
            "Millbrook seemed to explode. Umbrellas flew. Grace disappeared beneath a pile of teammates. The "
            "referee blew the final whistle before Rovers could even restart.\n\n"
            "Afterwards, as the team lifted the silver cup in the drizzle, their coach, Mr Adeyemi, found Hodan at "
            "the back of the crowd.\n\n"
            "“That pass,” he said, “was the best thing anyone did today. You know that, don't you?”\n\n"
            "Hodan grinned, her face streaked with mud. Over his shoulder she could see her grandad, who was still "
            "shouting her name."
        ),
        "qs": [
            {"id": "25359585b10d", "t": "mcq", "d": "infer", "q": "“Hodan's legs felt as if they were made of wet sand.” What does this suggest about how she felt?",
             "opts": ["She was exhausted and her legs felt heavy.",
                      "She had hurt her leg in a tackle.",
                      "She was cold because of the rain.",
                      "She was too nervous to move at all."],
             "why": "Wet sand is heavy and slumps; she had run more than in the whole season, so her legs felt tired and heavy."},
            {"id": "b8f3188e7a90", "t": "mcq", "d": "retrieve", "q": "Who scored Millbrook's first goal?",
             "opts": ["Priya", "Hodan", "Grace", "the Rovers captain"],
             "why": "The third paragraph says Hodan sent in a cross and Priya headed it in. The Rovers captain scored for the other team."},
            {"id": "d81df6f7b32b", "t": "tap", "d": "language", "q": "Tap the word that tells you how big the goalkeeper made herself look.",
             "s": "The goalkeeper came rushing out, arms wide, making herself [enormous].",
             "why": "Enormous means very big: with her arms wide, the goalkeeper made herself fill as much of the goal as she could."},
            {"id": "f20c5ba45c93", "t": "mcq", "d": "infer", "q": "Why did Hodan pass to Grace instead of shooting?",
             "opts": ["Grace had a much better chance of scoring than she did.",
                      "Hodan was too tired to kick the ball any further.",
                      "Mr Adeyemi had shouted at her to pass the ball.",
                      "Hodan had never wanted to score in a final."],
             "why": "Hodan was at a difficult angle with the goalkeeper rushing out, while Grace was unmarked with an empty goal. She had dreamed of scoring, so she put the team first."},
            {"id": "bcb3b80b7b8b", "t": "mcq", "d": "structure", "q": "Why does the writer put “She passed.” in a paragraph of its own?",
             "opts": ["to make Hodan's decision stand out as the key moment",
                      "to show that Hodan passed the ball very slowly",
                      "to start describing a different match",
                      "to show that Grace was a long way away from Hodan"],
             "why": "A two-word paragraph after the long build-up makes the reader stop: this choice is the turning point of the story."},
            {"id": "e12ed8cf1c9d", "t": "order", "d": "sequence", "q": "Put these events in the order they happen in the match.",
             "items": ["The Rovers captain scored.",
                       "Priya headed in Hodan's cross.",
                       "Hodan reached the loose ball near halfway.",
                       "Grace scored the winning goal.",
                       "The referee blew the final whistle."],
             "why": "Rovers scored in the first five minutes, Priya equalised before half-time, then in the last two minutes Hodan's run led to Grace's goal and the whistle."},
            {"id": "8883cb54eeb2", "t": "mcq", "d": "summarise", "q": "Which title would best sum up the story?",
             "opts": ["The Pass That Won the Cup", "Rovers Stay Unbeaten",
                      "Grandad's Umbrella", "A Muddy Training Session"],
             "why": "The story builds up to Hodan's unselfish pass, which wins the final. Rovers lose, and it is a final, not a training session."},
        ],
    },
    {
        "key": "RD6.14",
        "year": 6,
        "strand": "News reports",
        "title": "Families leave cliff-top homes",
        "nc": "Identify how language, structure and presentation contribute to meaning; retrieve and record information",
        "text": (
            "Families in the cliff-top village of Haverby, on the east coast of England, were told to leave their "
            "homes yesterday after a stretch of cliff as long as a football pitch fell into the sea during a night "
            "of fierce storms.\n\n"
            "Nobody was hurt in the fall, which happened at around 3 a.m. on Tuesday. However, the edge of the "
            "cliff is now just eight metres from the nearest of the five houses on Seaview Road, and the local "
            "council has decided that it is no longer safe for families to stay.\n\n"
            "“We heard a deep rumble, like a lorry going past, and the whole house shook,” said Margaret Hollis, "
            "74, who has lived on Seaview Road for more than forty years. “When it got light, I looked out of the "
            "back window, and half of my neighbour's garden had simply gone.”\n\n"
            "Haverby stands on one of the fastest-shrinking coastlines in Europe. The cliffs here are made of "
            "boulder clay, a soft mixture of clay, sand and stones left behind by glaciers at the end of the last "
            "Ice Age. Unlike hard rock, boulder clay is easily worn away. Waves pound the bottom of the cliff, "
            "scooping out the soft material, until the cliff above loses its support and slumps onto the beach. "
            "Heavy rain makes matters worse by soaking into the clay and making it heavier and weaker.\n\n"
            "Dr Sanjay Mehta, a coastal scientist at a nearby university, explained that erosion here is nothing "
            "new. “This coast has been retreating for thousands of years,” he said. “Whole villages that once stood "
            "here are now under the sea. What we are seeing is a natural process, but stronger storms can make "
            "sudden, large falls like this one more likely.”\n\n"
            "Some residents have called for a sea wall, or a barrier of large boulders known as rock armour, to be "
            "built at the foot of the cliff. These defences absorb the energy of the waves before they reach the "
            "cliff. However, they are expensive, and experts warn that protecting one stretch of coast can make "
            "erosion worse further along, where the beach is starved of sand.\n\n"
            "A spokesperson for the council said that the families would be offered temporary homes and that a "
            "meeting would be held next week to discuss the future of the village.\n\n"
            "For Mrs Hollis, the news is hard to accept. “I always knew the sea would come one day,” she said. “I "
            "just thought I'd have a bit longer.”"
        ),
        "qs": [
            {"id": "a7db97dae187", "t": "mcq", "d": "structure", "q": "What is the main job of the first paragraph of this report?",
             "opts": ["to sum up what happened, where and when",
                      "to explain what boulder clay is made of",
                      "to give the opinion of a coastal scientist",
                      "to describe Mrs Hollis's house and garden"],
             "why": "Like most news reports, it opens with the key facts: who (families in Haverby), what (told to leave after a cliff fell into the sea) and when (yesterday, after a night of storms)."},
            {"id": "56ef4af1b3a0", "t": "mcq", "d": "retrieve", "q": "How far is the edge of the cliff now from the nearest house on Seaview Road?",
             "opts": ["eight metres", "five metres", "forty metres", "the length of a football pitch"],
             "why": "The second paragraph says the edge is just eight metres from the nearest of the five houses. The football pitch is the length of cliff that fell."},
            {"id": "33e8f7355bde", "t": "order", "d": "sequence", "q": "Put these stages of the cliff fall in order, as the text explains them.",
             "items": ["Waves pound the bottom of the cliff.",
                       "The soft material at the bottom is scooped out.",
                       "The cliff above loses its support.",
                       "The cliff slumps onto the beach."],
             "why": "The fourth paragraph describes the process step by step: waves pound and scoop out the bottom until the cliff above has no support and slumps."},
            {"id": "4814d78a611e", "t": "tap", "d": "vocab", "q": "Tap the word that means “sinks down or falls heavily”.",
             "s": "Waves pound the bottom of the cliff, scooping out the soft material, until the cliff above loses its support and [slumps] onto the beach.",
             "why": "To slump is to sink or fall down heavily, as the unsupported cliff does."},
            {"id": "a2699b07dd24", "t": "mcq", "d": "infer", "q": "Why does Dr Mehta mention villages that are now under the sea?",
             "opts": ["to show that this coast has been wearing away for a very long time",
                      "to warn that Haverby will be under the sea by next week",
                      "to suggest that the storms on Tuesday destroyed other villages",
                      "to explain why boulder clay is harder than other rock"],
             "why": "He says erosion here is nothing new and the coast has been retreating for thousands of years; lost villages are the evidence."},
            {"id": "2c7f82515390", "t": "mcq", "d": "retrieve", "q": "According to the text, what is one problem with building rock armour?",
             "opts": ["It can make erosion worse further along the coast.",
                      "It makes the waves hit the cliff even harder.",
                      "It soaks up the rain and weakens the clay.",
                      "It takes thousands of years to build."],
             "why": "The sixth paragraph says defences are expensive and protecting one stretch can make erosion worse further along, where the beach is starved of sand."},
            {"id": "fd1f019f061a", "t": "mcq", "d": "infer", "q": "“I just thought I'd have a bit longer.” What does this suggest about how Mrs Hollis feels?",
             "opts": ["sad that she must leave sooner than she expected",
                      "surprised that the sea had ever reached the village",
                      "pleased to be offered a temporary home at last",
                      "angry with her neighbour about the lost garden"],
             "why": "She always knew the sea would come, so she is not surprised; she is sad that it has happened sooner than she hoped."},
        ],
    },
    {
        "key": "RD6.15",
        "year": 6,
        "strand": "Information",
        "title": "Climate zones and mountains",
        "nc": "Retrieve, record and present information from non-fiction; predict what might happen from details stated and implied",
        "text": (
            "If you could fly from the North Pole to the Equator, you would pass over a series of very different "
            "climates. Geographers divide the world into climate zones: large areas that share a similar pattern of "
            "weather over many years. Climate is not the same as weather. Weather is what happens on a particular "
            "day, such as a rainy Tuesday; climate is the usual weather of a place, measured over thirty years or "
            "more.\n\n"
            "Near the poles lie the polar zones, where it is bitterly cold for most of the year and very little "
            "grows. Further from the poles are the temperate zones, which include the United Kingdom. Here, summers "
            "are mild, winters are cool, and rain can fall at any time of year. Around the Equator lies the "
            "tropical zone, where the Sun is high in the sky all year round. Many tropical places are hot and very "
            "wet, which is perfect for rainforests. Along the edges of the tropics lie the great hot deserts, such "
            "as the Sahara, where it may not rain for years.\n\n"
            "Distance from the Equator is not the only thing that shapes a climate. Height matters too. As you "
            "climb a mountain, the air becomes thinner and colder: the temperature drops by several degrees for "
            "every thousand metres you climb. This is why Mount Kilimanjaro in Tanzania, which lies close to the "
            "Equator, has ice and snow on its summit, even though the plains around it are hot.\n\n"
            "Because of this, a tall mountain can hold several climates stacked one above another. At its foot "
            "there may be farmland or forest. Higher up, the trees grow shorter and then stop altogether at a point "
            "called the tree line. Above that come grassy slopes, then bare rock and, on the highest peaks, snow "
            "that never melts.\n\n"
            "Mountains also change the weather around them. When moist air blown in from the sea meets a mountain "
            "range, it is forced to rise. As it rises, it cools, and the water in it forms clouds and falls as "
            "rain. By the time the air has crossed the mountains, it has lost most of its moisture, so the land on "
            "the far side stays much drier. This dry area is called a rain shadow. In the UK, the wettest places "
            "are in the mountains of the west, such as those in Wales, the Lake District and Scotland, while many "
            "places in the east are much drier.\n\n"
            "Understanding climate zones and mountains helps to explain why people around the world live, farm and "
            "dress in such different ways."
        ),
        "qs": [
            {"id": "3278f63d7d46", "t": "mcq", "d": "compare", "q": "According to the text, how is climate different from weather?",
             "opts": ["Climate is the usual weather over many years; weather is what happens on one day.",
                      "Climate is what happens on one day; weather is the usual pattern over many years.",
                      "Climate is only found near the Equator; weather happens everywhere.",
                      "Climate is about rain; weather is about how hot or cold it is."],
             "why": "The first paragraph says weather is what happens on a particular day, while climate is the usual weather measured over thirty years or more."},
            {"id": "1665cb7d674e", "t": "mcq", "d": "retrieve", "q": "Which climate zone does the text say the United Kingdom is in?",
             "opts": ["temperate", "polar", "tropical", "desert"],
             "why": "The second paragraph says the temperate zones include the United Kingdom, with mild summers and cool winters."},
            {"id": "b96066ba8a06", "t": "mcq", "d": "infer", "q": "Why is it surprising that Mount Kilimanjaro has snow on its summit?",
             "opts": ["It lies close to the Equator, where the land around it is hot.",
                      "It is in the polar zone, where snow never falls at all.",
                      "It is the only mountain in the whole of Tanzania.",
                      "It is in a rain shadow, so it should stay dry."],
             "why": "Places near the Equator are usually hot, and the plains around Kilimanjaro are hot; the snow is there only because the summit is so high."},
            {"id": "aabe989aee1a", "t": "text", "d": "retrieve", "q": "Find and copy the name for the point on a mountain where trees stop growing.",
             "a": ["the tree line", "tree line", "treeline", "the treeline", "tree-line", "the tree-line"],
             "why": "The fourth paragraph says the trees stop altogether at a point called the tree line."},
            {"id": "51102f495b6c", "t": "order", "d": "sequence", "q": "Put these in order, from the foot of a tall mountain to the top.",
             "items": ["farmland or forest", "the tree line", "grassy slopes", "bare rock", "snow that never melts"],
             "why": "The fourth paragraph climbs the mountain: farmland or forest at the foot, the tree line, grassy slopes, bare rock, then snow on the highest peaks."},
            {"id": "8e9fad8dbed0", "t": "tap", "d": "vocab", "q": "Tap the word that means “damp” or “containing water”.",
             "s": "When [moist] air blown in from the sea meets a mountain range, it is forced to rise.",
             "why": "Moist means slightly wet: this air carries water from the sea, which later falls as rain."},
            {"id": "f57dc09fb335", "t": "mcq", "d": "predict", "q": "A town lies on the far side of a mountain range from the sea, and the wind blows from the sea. Using the text, what is its weather likely to be like?",
             "opts": ["drier than on the side facing the sea",
                      "wetter than on the side facing the sea",
                      "colder than the summit of the mountains",
                      "snowy all year round, like the peaks"],
             "why": "The air drops its rain as it rises over the mountains, so the far side is in a rain shadow and stays much drier."},
        ],
    },
    {
        "key": "RD6.16",
        "year": 6,
        "strand": "Persuasive writing",
        "title": "Walk to School Week",
        "nc": "Distinguish between statements of fact and opinion; identify how language contributes to meaning",
        "text": (
            "Are you ready to put your best foot forward? From Monday 2nd March, Greenfield Primary School is "
            "taking part in Walk to School Week, and we want every single family to join in!\n\n"
            "Every morning, hundreds of cars crawl along Station Road, queuing at the school gates, filling the air "
            "with fumes and making the crossing dangerous for our youngest children. We believe there is a better "
            "way. Imagine a street where the only traffic jam is a crowd of chatting friends.\n\n"
            "Walking is one of the simplest ways to stay healthy. Just fifteen minutes of brisk walking each way "
            "gets your heart pumping and your lungs working, and it adds up to more than two hours of exercise "
            "every week. Doctors advise that children should be active for at least an hour a day, and the walk to "
            "school is a brilliant head start. Even better, children who walk arrive at school awake, alert and "
            "ready to learn.\n\n"
            "Walking is good for our planet, too. Fewer car journeys mean cleaner air outside our school, where "
            "hundreds of young lungs breathe every day. And it costs absolutely nothing!\n\n"
            "Live too far away to walk the whole way? No problem. Try our Park and Stride scheme: park at Greenfield "
            "Leisure Centre, just ten minutes' walk from school, and walk the rest of the way with friends. Members "
            "of staff will be waiting at the leisure centre from 8.15 a.m. each morning to walk with any child whose "
            "family has signed up.\n\n"
            "Every child who walks, scoots or cycles to school at least three times during the week will receive a "
            "special badge, and the class with the most walkers will win an extra afternoon of outdoor games. Last "
            "year, Class 4 won by a single walker. Could it be your class this year?\n\n"
            "So dust off your trainers, pack an umbrella and join us for Walk to School Week. Your legs, your lungs "
            "and your local streets will thank you!\n\n"
            "To sign up for Park and Stride, please return the slip at the bottom of this leaflet to the school "
            "office by Friday 27th February."
        ),
        "qs": [
            {"id": "24eabc4bb598", "t": "mcq", "d": "vocab", "q": "“Are you ready to put your best foot forward?” What does this phrase mean here?",
             "opts": ["to make a real effort and get started",
                      "to step forward with your right foot first",
                      "to buy a new pair of shoes for school",
                      "to win a race by a single step"],
             "why": "To put your best foot forward is to make a good effort; it is also a play on words, because the leaflet is about walking."},
            {"id": "3eef0dddf396", "t": "tap", "d": "language", "q": "Tap the verb that shows how slowly the cars move along Station Road.",
             "s": "Every morning, hundreds of cars [crawl] along Station Road, queuing at the school gates, filling the air with fumes and making the crossing dangerous for our youngest children.",
             "why": "To crawl is to move very slowly, like a baby on hands and knees: the cars are stuck in a queue."},
            {"id": "9b5beaf6afd6", "t": "mcq", "d": "retrieve", "q": "According to the leaflet, how much exercise does walking to school add up to each week?",
             "opts": ["more than two hours", "fifteen minutes", "at least an hour", "ten minutes"],
             "why": "The third paragraph says fifteen minutes each way adds up to more than two hours of exercise every week. An hour a day is what doctors advise."},
            {"id": "d71d1208b4fa", "t": "mcq", "d": "purpose", "q": "Which of these is an opinion, not a fact?",
             "opts": ["We believe there is a better way.",
                      "Walk to School Week starts on Monday 2nd March.",
                      "Last year, Class 4 won by a single walker.",
                      "Staff will be waiting at the leisure centre."],
             "why": "“We believe” shows a point of view that others might not share. The other sentences give dates and events that can be checked."},
            {"id": "38de73208bbd", "t": "text", "d": "retrieve", "q": "Where should families taking part in Park and Stride park? Find and copy.",
             "a": ["Greenfield Leisure Centre", "the leisure centre", "leisure centre", "at Greenfield Leisure Centre"],
             "why": "The fifth paragraph says to park at Greenfield Leisure Centre, ten minutes' walk from school.",
             "no": {"Station Road": "Station Road is where the cars queue at the gates: the leaflet wants fewer cars there."}},
            {"id": "123a9d474c49", "t": "mcq", "d": "infer", "q": "Why does the writer mention that Class 4 won by a single walker last year?",
             "opts": ["to show that every child who walks could make the difference",
                      "to show that Class 4 is the healthiest class in the school",
                      "to warn that only one child from each class may take part",
                      "to explain why the competition is not being held this year"],
             "why": "If one walker decided the winner, then any child could help their class win: the writer is encouraging everyone to join in."},
            {"id": "1dfd2e38e206", "t": "mcq", "d": "purpose", "q": "Who is this leaflet mainly written for?",
             "opts": ["families of children at Greenfield Primary",
                      "drivers who use Station Road",
                      "doctors who look after children",
                      "staff at Greenfield Leisure Centre"],
             "why": "It speaks to “every single family”, mentions “your class” and asks families to return a sign-up slip to the school office."},
        ],
    },
]
