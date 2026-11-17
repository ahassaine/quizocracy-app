"""Reading comprehension, Year 9 (keys RD9.xx).

Twelve original passages, written by hand, as the bridge from KS3 reading to GCSE English Language.
The questions ask what the GCSE papers ask (what you learn from a section, how the writer uses language,
how the text is structured to interest the reader, a reader's evaluation of a statement, the writer's
attitudes compared), but as mcq, tap, find-and-copy and order questions, never essays. Terms met:
semantic field, personification, tone shift, cyclical structure, unreliable narrator, emotive language,
rhetorical question, counter-argument.

* RD9.01 a 19th-century-style description of a London street (story)
* RD9.02 the history of the NHS (information)
* RD9.03 a 19th-century-style letter from a traveller crossing the Alps (letter)
* RD9.04 a modern thriller-style chase through Hong Kong, without violence (story)
* RD9.05 the ethics of artificial intelligence, for teenagers (explanation)
* RD9.06 'The First Bus', a poem with a cyclical structure (poem)
* RD9.07 Alan Turing and the codebreakers of Bletchley Park (biography)
* RD9.08 a reflective coming-of-age moment on a Welsh beach (story)
* RD9.09 glaciers and a warming climate (information)
* RD9.10 a speech to a school assembly about CPR and defibrillators (persuasive)
* RD9.11 a dystopian-style scene with an unreliable narrator, without horror (story)
* RD9.12 a magazine feature on the economics of fast fashion (information)

Non-fiction facts are limited to well-established ones taught in English schools; uncertain numbers are
left out. To be reviewed line by line by a second reader before release.
"""

SKILLS = [
    {
        "key": "RD9.01",
        "year": 9,
        "strand": "Stories",
        "title": "A street by the river",
        "nc": "Know how language, including figurative language and vocabulary choice, presents meaning in fiction from the 19th century",
        "text": "There is a street in the eastern part of London, not far from the river, which the respectable traveller would do well to avoid at the close of a November afternoon, and which I, being neither very respectable nor very wise, have walked a hundred times. It is a narrow street, and an old one, and it has the air of a thing that was once young and has forgotten how.\n\n"
                "By four o'clock the fog has come up from the water. It does not arrive all at once, as rain does, but creeps along the gutters and climbs the area railings and lays itself, thick and yellow, against every window, until the shopkeepers inside are no more than shadows bending over their counters. The gas lamps are lit early, and each one hangs in the murk like a small, sickly moon, giving out a great deal of glow and very little light.\n\n"
                "And yet the street is never quiet. A costermonger pushes his barrow over the cobbles, crying his turnips and his onions in a voice made hoarse by twenty winters. A boy with no coat and an enormous cap darts between the cart-wheels with a bundle of newspapers, shouting the day's news to people who cannot see him. Somewhere a dog barks, and somewhere else a baby answers it. The baker at the corner, a broad, floury man who has never in his life been seen without his apron, stands in his doorway and watches it all with the calm satisfaction of one whose oven is warm.\n\n"
                "It is the smell of that oven, I think, that keeps me coming back. The fog smells of coal smoke and the river and something sour that I have never been able to name; but for ten yards on either side of the baker's door, the air is sweet with new bread, and the passers-by slow their steps without knowing why. Even the costermonger stops crying his onions there, as if out of respect.\n\n"
                "I have heard it said that such streets are a disgrace to a great city, and that they ought to be pulled down and something better built in their place. Perhaps they ought. The houses lean, the drains are a scandal, and half the children go to bed hungry. But I confess that when the lamplighter comes along with his long pole, and the windows glow one by one through the yellow gloom, I cannot wholly wish it gone. There is life in it, stubborn and noisy and warm, and I have found less in many a finer place.",
        "qs": [
            {"id": "4650f8fb2ee2", "t": "mcq", "d": "infer", "q": "What do you learn about the narrator from the first paragraph?",
             "opts": ["They know the street well and ignore its bad name", "They have only just arrived in London",
                      "They keep a shop in the street", "They avoid the street on winter afternoons"],
             "why": "The narrator has 'walked a hundred times' down a street that respectable people avoid, so they know it well and do not mind its reputation.",
             "no": {"They avoid the street on winter afternoons": "It is the 'respectable traveller' who would avoid it; the narrator says they have walked it a hundred times."}},
            {"id": "dcd9439e6cfe", "t": "mcq", "d": "retrieve", "q": "According to the second paragraph, how does the fog arrive?",
             "opts": ["Slowly, creeping along the gutters", "All at once, the way rain does",
                      "Suddenly, blown in by a wind", "Only once the gas lamps are lit"],
             "why": "The second paragraph says it 'does not arrive all at once, as rain does, but creeps along the gutters'."},
            {"id": "e7ef9a41dd27", "t": "tap", "d": "language", "q": "The writer uses personification to make the fog seem alive. Tap the three verbs that show the fog moving like a living thing.",
             "s": "It does not arrive all at once, as rain does, but [creeps] along the gutters and [climbs] the area railings and [lays] itself, thick and yellow, against every window, until the shopkeepers inside are no more than shadows bending over their counters.",
             "why": "Creeps, climbs and lays itself are things a living creature does, so the fog seems to move through the street as if it were alive."},
            {"id": "e5af35e662ef", "t": "mcq", "d": "vocab", "q": "Judging from the third and fourth paragraphs, what is a costermonger?",
             "opts": ["A street seller of fruit and vegetables", "A man who lights the street lamps",
                      "A boy who sells newspapers", "A baker who sells bread at his door"],
             "why": "He pushes a barrow and is 'crying his turnips and his onions': he sells vegetables in the street.",
             "no": {"A man who lights the street lamps": "That is the lamplighter, who comes in the last paragraph with his long pole."}},
            {"id": "51aa1bd4563c", "t": "mcq", "d": "retrieve", "q": "What happens near the baker's door, according to the fourth paragraph?",
             "opts": ["The costermonger stops calling out", "The fog becomes thicker and yellower",
                      "The newspaper boy stops to buy bread", "The narrator goes inside to get warm"],
             "why": "The fourth paragraph says 'Even the costermonger stops crying his onions there, as if out of respect.'"},
            {"id": "40c9fba12530", "t": "mcq", "d": "structure", "q": "How does the last paragraph change the focus of the passage?",
             "opts": ["From describing the street to judging it", "From the present to the narrator's childhood",
                      "From the street to the river nearby", "From the evening back to the morning"],
             "why": "The first four paragraphs describe the street; the last weighs up whether it should be pulled down and gives the narrator's own view."},
            {"id": "a1116a437a32", "t": "mcq", "d": "infer", "q": "A student wrote: 'The narrator thinks the street should be pulled down.' Which is the best response?",
             "opts": ["Not really: they admit its faults but cannot wish it gone", "Yes: they say the drains are a scandal",
                      "Yes: they call the street a disgrace to the city", "No: they think nothing in it needs to change"],
             "why": "The narrator admits the houses lean, the drains are bad and children go hungry, but says 'I cannot wholly wish it gone'.",
             "no": {"No: they think nothing in it needs to change": "The narrator does see faults: leaning houses, scandalous drains and hungry children.",
                    "Yes: they call the street a disgrace to the city": "The narrator has only 'heard it said' that such streets are a disgrace; it is other people's view."}},
        ],
    },
    {
        "key": "RD9.02",
        "year": 9,
        "strand": "Information",
        "title": "Free at the point of use: the story of the NHS",
        "nc": "Read a wide range of non-fiction critically: summarise and synthesise information, and follow the structure of an explanation",
        "text": "Before 1948, falling ill in Britain could be expensive as well as frightening. Many people had to pay to see a doctor, and many families put off calling one until it was too late. Some workers were covered by a national insurance scheme introduced in 1911, but their wives and children usually were not. Hospitals were a patchwork: some were run by local councils, others by charities that relied on donations, and the care a patient received could depend a great deal on where they lived and how much they could afford.\n\n"
                "During the Second World War, a government report written by the economist William Beveridge argued that Britain should tackle what he called five 'giants' standing in the way of a better life: want, disease, ignorance, squalor and idleness. A free health service was to be one of the main weapons against disease. After the war, the new Minister of Health, Aneurin Bevan, the son of a Welsh coal miner, took on the task of turning the idea into reality.\n\n"
                "It was not easy. Many doctors were worried about losing their independence and their income, and for a time their professional body opposed the plans. Bevan negotiated hard, and in the end most doctors agreed to join. On 5 July 1948 the National Health Service opened. For the first time, hospitals, family doctors, nurses, pharmacists, opticians and dentists were brought together into one service, paid for out of taxation and open to everyone. The central principle was that care should be free at the point of use: a patient would never be asked for money at the hospital door.\n\n"
                "Demand was enormous from the start. People who had gone without for years came forward for glasses, false teeth and treatment for long-standing complaints. The cost was far higher than planned, and within a few years the government introduced charges for glasses and false teeth, a decision so controversial that Bevan resigned from the government in protest. Charges for prescriptions followed soon afterwards.\n\n"
                "Since then, the NHS has changed in many ways. It has carried out the first heart transplants in Britain, given new vaccines to millions of children, and brought computers into every surgery. It has also faced constant arguments about money, waiting times and how it should be organised. Yet the founding principle has largely survived. Today the NHS is one of the largest employers in the world, and for many people in Britain it is a source of real pride: an idea, born in difficult times, that care should depend on need rather than on the ability to pay.",
        "qs": [
            {"id": "292789a7f0ac", "t": "mcq", "d": "retrieve", "q": "According to the first paragraph, who was usually left out of the 1911 insurance scheme?",
             "opts": ["Workers' wives and children", "Doctors who worked in hospitals",
                      "Families who lived in Wales", "Patients of charity hospitals"],
             "why": "The first paragraph says some workers were covered, 'but their wives and children usually were not'."},
            {"id": "7e35cc972b58", "t": "mcq", "d": "infer", "q": "Why does the writer call the hospitals before 1948 'a patchwork'?",
             "opts": ["They were a mix of many separate kinds, unevenly spread", "They were old buildings in need of repair",
                      "They were run by one body that covered the whole country", "They were mostly small and in the countryside"],
             "why": "A patchwork is made of many different pieces: some hospitals were run by councils, others by charities, and care depended on where you lived.",
             "no": {"They were run by one body that covered the whole country": "That is what the NHS did after 1948; before then, councils and charities ran different hospitals."}},
            {"id": "42f4157bc4e1", "t": "tap", "d": "retrieve", "q": "Tap the five 'giants' that Beveridge said stood in the way of a better life.",
             "s": "During the Second World War, a government report written by the economist William Beveridge argued that Britain should tackle what he called five 'giants' standing in the way of a better life: [want], [disease], [ignorance], [squalor] and [idleness].",
             "why": "The five giants are listed after the colon: want, disease, ignorance, squalor and idleness."},
            {"id": "da1a2f78a535", "t": "mcq", "d": "vocab", "q": "Which of Beveridge's 'giants' does 'squalor' mean?",
             "opts": ["Dirty, overcrowded living conditions", "Having no work to do",
                      "A lack of education", "Not having enough money for food"],
             "why": "Squalor is filth and bad housing. Idleness is having no work, ignorance is lack of education, and want is poverty."},
            {"id": "a8ebd11acff3", "t": "text", "d": "retrieve", "q": "Find and copy the word in the third paragraph that tells you how the NHS was paid for.",
             "a": ["taxation", "out of taxation", "taxes", "tax"],
             "why": "The third paragraph says the service was 'paid for out of taxation'."},
            {"id": "1a96c5e8257e", "t": "mcq", "d": "infer", "q": "What does the fourth paragraph suggest about many people's lives before 1948?",
             "opts": ["They had put up with health problems they could not afford to treat", "They already had glasses and false teeth but needed new ones",
                      "They had been treated free by doctors who later joined the NHS", "They did not trust the new service and stayed away from it"],
             "why": "People 'who had gone without for years' rushed forward: they had lived with problems because treatment had cost too much.",
             "no": {"They did not trust the new service and stayed away from it": "The text says the opposite: 'Demand was enormous from the start.'"}},
            {"id": "eb747809ae67", "t": "mcq", "d": "structure", "q": "How is the passage mainly organised?",
             "opts": ["In time order, from before 1948 to today", "As an argument, then a counter-argument",
                      "As a set of patients' own stories", "As a comparison of Britain with other countries"],
             "why": "It moves through time: life before 1948, the wartime report, the opening, the first years, and the NHS since then."},
        ],
    },
    {
        "key": "RD9.03",
        "year": 9,
        "strand": "Letters and diaries",
        "title": "A letter from the mountains",
        "nc": "Read 19th-century non-fiction; compare the attitudes and viewpoints of people in a text",
        "text": "Airolo, 14th June 1868\n\n"
                "My dear Thomas,\n\n"
                "You will forgive the shaking of my hand, for I write this by candlelight in a room so cold that I can see my own breath, and this in June. I promised you a full account of our crossing of the mountains, and you shall have it, though I fear you will think I have lost my senses.\n\n"
                "We left the lake at six in the morning, in a great yellow coach drawn by five horses, with a driver who sang the whole way and a guard who did not speak at all. Mrs Ashworth, who has been my companion since Paris, declared before we had gone a mile that the road was a disgrace and the seats a punishment, and she said very little else until noon. I confess that I was frightened too. The road climbs in such sharp bends that at every turn the leading horses seemed to hang over nothing at all, and far beneath us the river was no more than a white thread laid upon the rocks.\n\n"
                "But, Thomas, the mountains! I had read of them, and seen them in engravings, and believed myself prepared. I was not. They do not stand in a row like the hills at home; they crowd upon one another, peak behind peak, each one whiter and more distant than the last, until you cannot tell where the snow ends and the clouds begin. At the top of the pass we stopped at a poor stone inn, and I stood outside in the wind for a quarter of an hour, and could not make myself go in to dinner.\n\n"
                "Mrs Ashworth went in at once. She pronounced the soup thin, the bread stale, and the view 'a great deal of rock'. I do not blame her; she is past sixty and her bones ache in the cold. Yet I could not help thinking that she had travelled four hundred miles to look at the inside of an inn.\n\n"
                "The descent was quicker and, to my mind, worse. The driver let the horses run, and the coach swung so wildly from side to side that I held on to the window strap with both hands and shut my eyes, and opened them again only because I could not bear to miss anything.\n\n"
                "I do not know how to end this letter, except to say that I am glad, so very glad, that I came. Tell Mother that I am well wrapped up and eating properly, which is very nearly true.\n\n"
                "Your loving sister,\n"
                "Harriet",
        "qs": [
            {"id": "ae8d146e9bf8", "t": "mcq", "d": "retrieve", "q": "Why does Harriet ask Thomas to forgive the shaking of her hand?",
             "opts": ["She is writing in a very cold room", "She is still shaken by the descent",
                      "She is writing in the moving coach", "She hurt it holding the window strap"],
             "why": "She writes 'in a room so cold that I can see my own breath'.",
             "no": {"She is still shaken by the descent": "She was frightened on the way down, but the reason she gives for the shaking is the cold room."}},
            {"id": "a387a098ac71", "t": "mcq", "d": "language", "q": "From the coach, the river looks like 'a white thread laid upon the rocks'. What does this comparison mainly suggest?",
             "opts": ["How far below the road the river was", "How fast the river water was flowing",
                      "How cold the water in the river was", "How narrow the road beside it was"],
             "why": "A river only looks as thin as a thread from very high up, so the comparison suggests the frightening drop beneath the road."},
            {"id": "11a6a2e246eb", "t": "tap", "d": "language", "q": "Tap the verb that makes the mountains seem to push together like people in a busy place.",
             "s": "They do not stand in a row like the hills at home; they [crowd] upon one another, peak behind peak, each one whiter and more distant than the last, until you cannot tell where the snow ends and the clouds begin.",
             "why": "People crowd together in a busy place; 'crowd upon one another' makes the peaks seem packed and jostling, unlike hills standing in a tidy row."},
            {"id": "8db15866a210", "t": "mcq", "d": "vocab", "q": "'She pronounced the soup thin.' What does 'pronounced' mean here?",
             "opts": ["Declared as her firm opinion", "Said each sound clearly",
                      "Muttered quietly to herself", "Asked the innkeeper about"],
             "why": "To pronounce something thin, stale or dull is to announce your judgement of it, as Mrs Ashworth does with the soup, bread and view.",
             "no": {"Said each sound clearly": "That is another meaning of 'pronounce', for saying a word; here she is giving her verdict on the soup."}},
            {"id": "d040cc8c0e63", "t": "mcq", "d": "infer", "q": "What does Harriet suggest when she says Mrs Ashworth 'had travelled four hundred miles to look at the inside of an inn'?",
             "opts": ["Mrs Ashworth had wasted the chance to see the mountains", "Mrs Ashworth had come only to stay at famous inns",
                      "The inn was the finest sight of the whole journey", "Mrs Ashworth was too ill to leave the coach"],
             "why": "Mrs Ashworth went straight inside and called the view 'a great deal of rock', so Harriet gently mocks her for missing what they came to see."},
            {"id": "1941494b205c", "t": "mcq", "d": "structure", "q": "Where does the clearest tone shift in the letter come?",
             "opts": ["At 'But, Thomas, the mountains!', from fear to wonder", "At the descent, from wonder to boredom",
                      "At the inn, from wonder to anger", "At the last paragraph, from joy to regret"],
             "why": "Before it, Harriet describes her fear of the road; 'But, Thomas, the mountains!' turns the letter to amazement at the view.",
             "no": {"At the last paragraph, from joy to regret": "Harriet ends 'so very glad, that I came': there is no regret."}},
            {"id": "4bfb25806ded", "t": "mcq", "d": "compare", "q": "How do Harriet's and Mrs Ashworth's attitudes to the crossing compare?",
             "opts": ["Harriet is overwhelmed by the view; Mrs Ashworth is unimpressed", "Both are frightened at first but come to love the view",
                      "Harriet is bored by the view; Mrs Ashworth admires it", "Both find the mountains less striking than they expected"],
             "why": "Harriet stands outside for a quarter of an hour and cannot go in, while Mrs Ashworth calls the view 'a great deal of rock'.",
             "no": {"Both are frightened at first but come to love the view": "Only Harriet comes to love it; Mrs Ashworth complains about the road, the food and the view."}},
        ],
    },
    {
        "key": "RD9.04",
        "year": 9,
        "strand": "Stories",
        "title": "Delivery number nine",
        "nc": "Know how text structure and sentence length are used to build tension in modern fiction",
        "text": "The envelope is in Jun's inside pocket, flat against his ribs, and the man in the grey jacket is still behind him.\n\n"
                "Jun noticed him first at the ferry pier: a tall figure, a cap pulled low, a phone held to one ear but not, Jun thought, actually talking into it. Now, twelve minutes and three crowded streets later, the grey jacket is still there. Never closer than twenty metres. Never further than forty.\n\n"
                "Jun speeds up. The market on Fa Yuen Street is at its loudest, and he slides into it like a coin into a slot. Stalls of trainers and phone cases and plastic toys press in from both sides. A woman wheels a trolley of flattened cardboard across his path; he swerves, apologises, keeps going. Behind him, a shout. He does not look back.\n\n"
                "Delivery number nine. Mrs Lam at the Kowloon office. Before four o'clock, the dispatcher said, and do not let it out of your sight. It is three forty-one.\n\n"
                "He cuts left down an alley that smells of frying garlic, then right, past the open back doors of restaurants where cooks in white vests chop vegetables and argue. A cat watches him from a pile of crates. His trainers slap on the wet concrete. His heart is a drum. He knows these streets; he has run them every day for a year. The grey jacket does not. That is his only advantage.\n\n"
                "At the end of the alley, he stops dead.\n\n"
                "The man is there. Somehow, impossibly, he is standing at the corner, bent double, breathing like a broken bellows, one hand raised.\n\n"
                "'Wait,' he gasps. 'Please. Just wait.'\n\n"
                "Jun's mind races through his choices. Back down the alley. Into a restaurant kitchen. Up the fire escape. He takes one step backwards.\n\n"
                "The man fumbles in his jacket and holds something out. Another envelope: the same brown paper, the same company label, the same name written on the front.\n\n"
                "'You left the pier before I could give you this,' he says. 'Mrs Lam needs both of them. I've been shouting your name since Nathan Road.'\n\n"
                "For a long moment Jun simply stares at him. Then, slowly, he begins to laugh, and the man in the grey jacket, still struggling for breath, begins to laugh too.\n\n"
                "It is three forty-four. They walk the last two streets together.",
        "qs": [
            {"id": "face982dd9f1", "t": "mcq", "d": "infer", "q": "Why does Jun think the man at the pier is 'not actually talking' into his phone?",
             "opts": ["He suspects the call is a cover for watching him", "He can see that the phone is switched off",
                      "He hears the man speaking another language", "He thinks the man is waiting for Jun to ring"],
             "why": "The man stays a steady distance behind Jun for twelve minutes, so Jun suspects the phone is only a disguise while he follows."},
            {"id": "897dae5d47e0", "t": "mcq", "d": "retrieve", "q": "What does Jun believe is his 'only advantage'?",
             "opts": ["He knows the streets and the man does not", "He is younger and faster than the man",
                      "He has a head start of forty metres", "The market crowd hides him from view"],
             "why": "The text says 'He knows these streets... The grey jacket does not. That is his only advantage.'"},
            {"id": "e13e06e38c7d", "t": "mcq", "d": "language", "q": "The writer often uses very short sentences, such as 'Never closer than twenty metres.' and 'He does not look back.' What is their main effect?",
             "opts": ["They create a fast pace and build tension", "They show that Jun is not very clever",
                      "They slow the story down to calm the reader", "They give the man's point of view"],
             "why": "Short, clipped sentences read quickly, like Jun's running and racing thoughts, so the tension rises.",
             "no": {"They slow the story down to calm the reader": "Long, flowing sentences tend to slow a story; short ones speed it up."}},
            {"id": "ab721825cf0c", "t": "mcq", "d": "vocab", "q": "Who is 'the dispatcher' in the fourth paragraph most likely to be?",
             "opts": ["The person who gives couriers their jobs", "The customer who will receive the envelope",
                      "The man who has been following Jun", "The owner of a stall in the market"],
             "why": "The dispatcher told Jun the delivery time and the rule about the envelope: a dispatcher sends couriers out on their jobs.",
             "no": {"The customer who will receive the envelope": "That is Mrs Lam at the Kowloon office."}},
            {"id": "07771917d3d5", "t": "order", "d": "sequence", "q": "Put these events in the order they happen in the story.",
             "items": ["Jun notices the man at the ferry pier", "Jun hurries through the market on Fa Yuen Street",
                       "Jun runs down an alley that smells of garlic", "The man holds out a second envelope",
                       "Jun and the man walk on together"],
             "why": "The pier comes first (told as a memory), then the market, the alley, the meeting at the corner and the walk together."},
            {"id": "2c0375d0c540", "t": "mcq", "d": "structure", "q": "How does the writer structure the story to interest the reader?",
             "opts": ["Builds suspense, then reveals the follower meant no harm", "Starts at the ending, then explains how it came about",
                      "Tells the chase twice, once from each man's view", "Moves between the chase and Jun's memories of school"],
             "why": "For most of the story we fear the man in the grey jacket; the twist near the end shows he was only bringing the second envelope."},
            {"id": "e94988d0544c", "t": "mcq", "d": "infer", "q": "Why do Jun and the man both laugh at the end?",
             "opts": ["They are relieved the chase was a misunderstanding", "They both find the envelope's label funny",
                      "Jun is mocking the man for being so slow", "They realise they are too late for Mrs Lam"],
             "why": "Jun thought he was being chased and the man thought Jun was ignoring him; the laughter is relief once they understand.",
             "no": {"They realise they are too late for Mrs Lam": "It is only three forty-four, and the deadline is four o'clock."}},
        ],
    },
    {
        "key": "RD9.05",
        "year": 9,
        "strand": "Explanations",
        "title": "Thinking about artificial intelligence",
        "nc": "Read critically: recognise a writer's viewpoint, a counter-argument and the rhetorical devices used to engage the reader",
        "text": "You have almost certainly used artificial intelligence today, whether or not you noticed. It may have suggested the next video you watched, sorted your messages, or finished a sentence as you typed. Newer AI tools can write essays, draw pictures and hold conversations that sound remarkably human. These are impressive achievements. But they also raise questions that are not about technology at all. They are about fairness, honesty and responsibility, and they are questions your generation will have to answer.\n\n"
                "Start with how these systems learn. Most modern AI is not programmed rule by rule. Instead, it is trained on enormous amounts of data, such as text, photographs or recordings, and it learns to spot patterns in them. This is powerful, but it means an AI can only be as good as the data it learns from. If a face-recognition system is trained mostly on photographs of one group of people, it may work less well for everyone else. Nobody needs to intend this unfairness for it to happen; it is simply copied from the data. This problem is known as bias.\n\n"
                "A second question is about truth. AI tools can now produce realistic photographs of events that never happened, or copy a person's voice from a short recording. Used for a film, or a joke between friends who are in on it, this can be harmless. Used to trick people, it is not. AI chatbots can also state false information with complete confidence, because they are built to produce answers that sound likely, not to check facts. The sensible habit is the one good historians have always had: ask where a claim came from before you believe it.\n\n"
                "Then there is responsibility. If a self-driving car makes a mistake, or a computer system wrongly turns down someone's application for a job, who is to blame? The programmers? The company that sold it? The person who chose to use it? In many countries the law is still catching up with questions like these.\n\n"
                "Some people argue that worrying about all this is pointless, since the technology is coming whether we like it or not. There is some truth in that: AI is unlikely to disappear. But tools are shaped by the choices of the people who build and use them. Cars, for example, arrived long before driving tests, the Highway Code and seat belts, and those rules were argued over and agreed by people. The same can happen here.\n\n"
                "So what does this mean for you? It means using AI as a helper, not as a replacement for your own thinking: an essay you did not write teaches you nothing, however good it looks. It means thinking twice before uploading photographs of your friends. And it means asking questions. The people who will decide how AI is used in twenty years' time are sitting in classrooms now.",
        "qs": [
            {"id": "e9965e1dc416", "t": "mcq", "d": "retrieve", "q": "According to the first paragraph, what are the questions raised by AI really about?",
             "opts": ["Fairness, honesty and responsibility", "Speed, cost and computer storage",
                      "Videos, messages and typing", "Essays, pictures and conversations"],
             "why": "The first paragraph says the questions 'are about fairness, honesty and responsibility'.",
             "no": {"Essays, pictures and conversations": "Those are things newer AI tools can make; the questions they raise are about something else."}},
            {"id": "c8de0581a8c4", "t": "text", "d": "retrieve", "q": "Find and copy the one-word name the writer gives to unfairness that an AI copies from its training data.",
             "a": ["bias"],
             "why": "The second paragraph ends: 'This problem is known as bias.'"},
            {"id": "3e4468e706d3", "t": "mcq", "d": "infer", "q": "What does the writer mean by 'Nobody needs to intend this unfairness for it to happen'?",
             "opts": ["An AI can become unfair by accident, through its data", "The programmers secretly wanted the system to be unfair",
                      "Unfair systems are always noticed and fixed at once", "Only careless companies ever build unfair systems"],
             "why": "The writer says the unfairness 'is simply copied from the data': it can happen without anyone meaning it to."},
            {"id": "9db2ead23999", "t": "mcq", "d": "vocab", "q": "In the fourth paragraph, the law is 'still catching up' with questions about AI. What does this phrase mean here?",
             "opts": ["It has not yet settled these new problems", "It is changing faster than the technology",
                      "It is chasing companies that have broken it", "It has already answered every question"],
             "why": "To catch up is to reach something that got ahead: the technology has moved faster than the law, which has not yet decided who is to blame."},
            {"id": "e42d76db1023", "t": "mcq", "d": "language", "q": "Why does the writer use a run of rhetorical questions in the fourth paragraph ('The programmers? The company that sold it?')?",
             "opts": ["To show the answer is unclear and make readers think", "To test the reader's knowledge of the law",
                      "To prove that the programmers are to blame", "To show the writer does not care who is to blame"],
             "why": "Rhetorical questions are not meant to be answered aloud; here they show how many people could be blamed and leave the reader weighing them up.",
             "no": {"To prove that the programmers are to blame": "The programmers are only the first of three possible answers, and the writer does not choose between them."}},
            {"id": "444d66df57d0", "t": "mcq", "d": "structure", "q": "What does the fifth paragraph do in the writer's argument?",
             "opts": ["It gives a counter-argument and then answers it", "It sums up the three questions raised so far",
                      "It tells a story about a self-driving car", "It explains how an AI is trained on data"],
             "why": "It starts with what 'some people argue' (worrying is pointless), admits 'some truth in that', then answers it with the example of cars."},
            {"id": "ce8e4870d997", "t": "mcq", "d": "purpose", "q": "What is the writer's main purpose?",
             "opts": ["To help teenagers think about using AI wisely", "To persuade teenagers never to use AI tools",
                      "To explain how to build an AI chatbot", "To argue that AI will soon disappear"],
             "why": "The writer explains the questions AI raises and ends with advice for 'you': use it as a helper, think twice, ask questions.",
             "no": {"To persuade teenagers never to use AI tools": "The writer suggests 'using AI as a helper', not avoiding it altogether."}},
        ],
    },
    {
        "key": "RD9.06",
        "year": 9,
        "strand": "Poems",
        "title": "The First Bus",
        "nc": "Read poetry critically: how imagery, semantic fields and a cyclical structure present the poet's ideas",
        "text": "At ten to five the first bus leaves the depot,\n"
                "its windows bright as an open fridge,\n"
                "its engine clearing its throat in the dark.\n\n"
                "The driver, Delroy, knows the road by heart:\n"
                "the speed bump by the launderette,\n"
                "the bend where the foxes cross.\n\n"
                "It stops for a cleaner in a padded coat\n"
                "who sits at the back with her eyes shut,\n"
                "still holding a dream she has not finished.\n\n"
                "It stops for a baker, flour on his cuffs,\n"
                "for two nurses sharing one pair of earphones,\n"
                "for a boy with a toolbag nearly as big as himself.\n\n"
                "It stops for a woman with a bucket of flowers\n"
                "she will sell by the station before the trains start,\n"
                "and for an old man who gets on every morning\n"
                "and never says where he is going.\n\n"
                "It stops for a student with a rucksack\n"
                "who has worked all night at a petrol station\n"
                "and falls asleep before the second stop.\n\n"
                "Nobody speaks. The heater hums.\n"
                "The city slides past in orange and black,\n"
                "the shop shutters down like closed eyelids,\n"
                "the tower blocks asleep on their feet.\n\n"
                "At the hospital the nurses get off together,\n"
                "still sharing their music, one earphone each,\n"
                "and walk towards the lit doors\n"
                "where the night shift is waiting to go home.\n\n"
                "By six the sky is the colour of dishwater,\n"
                "then milk, then a thin and hopeful blue,\n"
                "and one by one the others ring the bell and go,\n\n"
                "each of them stepping down into a day\n"
                "that would not open without them:\n"
                "the swept floors, the warm loaves,\n"
                "the mended pipes, the morning flowers.\n\n"
                "Later, the city will wake to clean offices,\n"
                "to fresh bread on the shelves and water in the taps,\n"
                "and will not stop to wonder how they got there,\n"
                "or who was up before the birds to make it so.\n\n"
                "And the bus turns back the way it came,\n"
                "empty again, still bright, still humming,\n"
                "and Delroy yawns and checks the time,\n\n"
                "because tomorrow, at ten to five,\n"
                "when the road is dark and the foxes are crossing,\n"
                "the first bus leaves the depot.",
        "qs": [
            {"id": "42e618964d85", "t": "text", "d": "retrieve", "q": "Which animals cross the road at the bend that Delroy knows? Find and copy the word.",
             "a": ["foxes", "the foxes", "fox", "a fox"],
             "why": "The second verse says Delroy knows 'the bend where the foxes cross'."},
            {"id": "790e72af2bb8", "t": "mcq", "d": "infer", "q": "In its most literal sense, what does 'still holding a dream she has not finished' tell us about the cleaner?",
             "opts": ["She had to get up before she was ready", "She has just been given some bad news",
                      "She has been awake all through the night", "She is reading a book on the journey"],
             "why": "A dream she 'has not finished' means her sleep was cut short; with her eyes shut, she is still half asleep.",
             "no": {"She has been awake all through the night": "That is the student. The cleaner was dreaming, so she had been asleep."}},
            {"id": "c50a1baf4876", "t": "mcq", "d": "retrieve", "q": "What will the woman with the bucket of flowers do with them?",
             "opts": ["Sell them by the station before the trains start", "Give them to the nurses at the hospital",
                      "Put them in the shops before they open", "Sell them at the market after work"],
             "why": "The fifth verse says they are flowers 'she will sell by the station before the trains start'."},
            {"id": "12eacc7a734b", "t": "tap", "d": "language", "q": "This sentence continues the poem's semantic field of sleep. Tap the part of a sleeping face that the shop shutters are compared to.",
             "s": "The city slides past in orange and black, the shop shutters down like closed [eyelids], the tower blocks asleep on their feet.",
             "why": "The shutters are pulled down 'like closed eyelids' and the tower blocks are 'asleep': like the cleaner's dream, the sleeping student and Delroy's yawn, they make the whole city seem asleep."},
            {"id": "4b7a0421d4d8", "t": "mcq", "d": "retrieve", "q": "Which passengers get off the bus together at the hospital?",
             "opts": ["The two nurses", "The cleaner and the baker",
                      "The student and the old man", "The boy and the flower seller"],
             "why": "The eighth verse says 'At the hospital the nurses get off together'."},
            {"id": "a2fb2f492b84", "t": "mcq", "d": "infer", "q": "What is the poet's attitude in the verse beginning 'Later, the city will wake'?",
             "opts": ["Sad that the early workers go unnoticed", "Angry with the passengers for not speaking",
                      "Delighted that the city is ready for the day", "Worried that the bus will be late tomorrow"],
             "why": "The city 'will not stop to wonder' who made its morning possible: the tone shifts to a quiet regret that these workers are not noticed or thanked."},
            {"id": "ff72d3c02c48", "t": "mcq", "d": "structure", "q": "Why can the poem's structure be called cyclical?",
             "opts": ["It ends where it began, with the bus leaving the depot", "Each verse is about a different passenger",
                      "It follows the bus from the first stop to the last", "Every verse has exactly the same number of lines"],
             "why": "The first and last lines both have the first bus leaving the depot at ten to five: the poem comes full circle, as the same journey happens every day.",
             "no": {"It follows the bus from the first stop to the last": "That would be a straight line from start to finish; a cyclical structure returns to where it started."}},
        ],
    },
    {
        "key": "RD9.07",
        "year": 9,
        "strand": "Biography",
        "title": "Alan Turing and the codebreakers",
        "nc": "Read non-fiction critically: retrieve and summarise information, and evaluate a statement using evidence from the text",
        "text": "In 1939, as Britain went to war, a quiet mathematician of twenty-seven arrived at a country house in Buckinghamshire called Bletchley Park. His name was Alan Turing, and the work he did there over the following years would remain secret for decades.\n\n"
                "The problem facing Bletchley Park was a machine called Enigma. The German armed forces used it to scramble their radio messages. An operator typed a message on its keyboard, and a set of rotating wheels inside turned each letter into a different one; because the wheels moved after every key press, the same letter could come out differently each time. The settings were changed every day, so even a code that had been cracked on Monday was useless by Tuesday. The number of possible settings was so vast that trying them one by one, by hand, was hopeless.\n\n"
                "Turing did not try to beat Enigma by hand. Building on earlier work by Polish mathematicians, who had shared their discoveries with Britain shortly before the war, he designed a machine called the Bombe. It worked from a short piece of text that the codebreakers guessed would appear in a message, such as a weather report or a standard greeting, and rapidly tested settings to rule out the ones that could not produce it. Each Bombe was a large cabinet of whirring drums, and many were eventually built and run by teams of operators, most of them women.\n\n"
                "Turing also led the work on naval Enigma, which protected the messages sent to German submarines in the Atlantic. Reading those messages helped Allied ships avoid attack and kept vital supplies of food and fuel crossing the ocean to Britain. Historians still debate exactly how much the codebreakers shortened the war, but few doubt that their contribution was enormous.\n\n"
                "Codebreaking was not the whole of Turing's achievement. Before the war, in 1936, he had written a paper describing an imaginary 'universal machine' that could carry out any calculation if it were given the right instructions. This idea lies at the heart of every computer we use today. After the war he worked on some of the earliest real computers, and in 1950 he asked a question that still provokes argument: could a machine think? He proposed a test, now named after him, in which a person holds written conversations and tries to tell whether they are talking to a human or a machine.\n\n"
                "Turing died in 1954, at the age of forty-one. Because of the secrecy around Bletchley Park, the public knew almost nothing of his wartime work for many years. Today he is widely recognised as one of the founders of computer science, and since 2021 his portrait has appeared on the Bank of England's fifty-pound note.",
        "qs": [
            {"id": "c40f2eb5ffbc", "t": "mcq", "d": "vocab", "q": "The German armed forces used Enigma 'to scramble their radio messages'. What does 'scramble' mean here?",
             "opts": ["Mix up so that they cannot be read", "Send out very quickly in an emergency",
                      "Shorten to save time on the radio", "Pass on to many places at once"],
             "why": "Enigma turned each letter into a different one, so 'scramble' means jumble the message until outsiders cannot read it."},
            {"id": "aab7b08e38e2", "t": "mcq", "d": "retrieve", "q": "Why did the daily change of settings make the codebreakers' task so hard?",
             "opts": ["A code cracked one day was useless the next", "Each change added a new wheel to the machine",
                      "The new settings were sent by a secret radio", "The operators changed the keyboard letters too"],
             "why": "The second paragraph says 'even a code that had been cracked on Monday was useless by Tuesday'."},
            {"id": "28be5b819ad8", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you the nationality of the mathematicians whose work Turing built on.",
             "s": "Building on earlier work by [Polish] mathematicians, who had shared their discoveries with Britain shortly before the war, he designed a machine called the Bombe.",
             "why": "Polish tells you where the mathematicians came from: Turing built on the work of Polish mathematicians, who shared their discoveries shortly before the war."},
            {"id": "edae07d24432", "t": "mcq", "d": "infer", "q": "Why did the codebreakers start from text such as a weather report or a standard greeting?",
             "opts": ["Some messages were likely to contain those words", "Weather reports were never sent in code",
                      "The Germans sent them to trick the codebreakers", "The Bombe could only work on weather reports"],
             "why": "A weather report or greeting was predictable, so the codebreakers could guess some words of a message and test settings against them."},
            {"id": "a27e0b6b9b48", "t": "text", "d": "retrieve", "q": "Find and copy the two words, in inverted commas, for the imaginary machine Turing described in 1936.",
             "a": ["universal machine", "a universal machine", "'universal machine'", "the universal machine"],
             "why": "The fifth paragraph says his 1936 paper described an imaginary 'universal machine'."},
            {"id": "95bad191e2b5", "t": "mcq", "d": "infer", "q": "A student wrote: 'Turing is important only because he helped to break Enigma.' Which detail from the text best challenges this view?",
             "opts": ["His 1936 idea lies at the heart of every computer", "He led the work on naval Enigma",
                      "He designed the Bombe with whirring drums", "His wartime work was kept secret for years"],
             "why": "The fifth paragraph opens 'Codebreaking was not the whole of Turing's achievement': his universal machine is the idea behind every computer today.",
             "no": {"He led the work on naval Enigma": "That is more codebreaking, so it supports the student's view rather than challenging it."}},
            {"id": "f94308ca7a3b", "t": "mcq", "d": "structure", "q": "Why does the writer begin with Turing arriving at Bletchley Park, not with his birth or childhood?",
             "opts": ["To open with his most dramatic and secret work", "Because nothing is known about his early life",
                      "Because the Bombe had already been built by then", "To show his work was quickly made public"],
             "why": "Starting in 1939, as Britain went to war, with work that 'would remain secret for decades', draws the reader in straight away.",
             "no": {"To show his work was quickly made public": "The text says the opposite: the public knew almost nothing of it for many years."}},
        ],
    },
    {
        "key": "RD9.08",
        "year": 9,
        "strand": "Stories",
        "title": "Skimming stones",
        "nc": "Make inferences about a first-person narrator's feelings, and know how a shift of tone and time changes meaning",
        "text": "The summer I was thirteen, my sister Ffion left for university, and on her last evening at home she asked me to walk down to the beach with her. I said no. I said it twice. Then Mam gave me the look that meant I was going whether I liked it or not, and I went, dragging my trainers through the sand as loudly as I could.\n\n"
                "I was angry with Ffion that whole summer, though I could not have told you why. She had been packing for weeks. Her half of our room had turned slowly into cardboard boxes, and every evening there were fewer of her things on the shelf: the photo of her netball team, the jar of shells, the radio she played too loudly at night. I told myself I was glad. I would have the room to myself. I would have the remote control to myself. I would have, I said to my friend Gethin, a bit of peace at last.\n\n"
                "The tide was out, and the beach at Rhossili went on for ever, flat and shining, the colour of wet slate. We walked right down to the edge of the water without saying a word. Ffion picked up a flat stone and skimmed it. It bounced four times. She handed me one, and mine sank at once, the way it always had, and she laughed, and I wanted to be furious about that too, but somehow I was not.\n\n"
                "'You know you're allowed to miss me,' she said.\n\n"
                "'I won't,' I said.\n\n"
                "'Okay.' She skimmed another stone. 'I'll miss you, though.'\n\n"
                "I remember that the sun was going down behind the headland, and that the sea had turned from grey to a kind of burning copper, and that I suddenly could not see it very clearly. I said something about the wind making my eyes water. Ffion did not say anything. She just put her arm round my shoulders, which she had not done since I was small, and we stood there until the water came up and touched our feet.\n\n"
                "I am older now than she was then. I have a jar of shells of my own, and a radio, and I know that what I felt on that beach was not anger at all. It was the first time I understood that the people you love do not stay exactly where you put them. Some evenings, when the light goes copper over the sea, I still try to skim a stone. It still sinks. I still laugh.",
        "qs": [
            {"id": "63e4eab21469", "t": "tap", "d": "retrieve", "q": "Three of Ffion's things are listed after the colon. Tap the first noun in each item of the list.",
             "s": "Her half of our room had turned slowly into cardboard boxes, and every evening there were fewer of her things on the shelf: the [photo] of her netball team, the [jar] of shells, the [radio] she played too loudly at night.",
             "why": "After the colon, the narrator lists three items: the photo of her netball team, the jar of shells and the radio. The first noun in each is photo, jar and radio."},
            {"id": "b6c7fb86986d", "t": "mcq", "d": "infer", "q": "When the narrator tells Gethin they will have 'a bit of peace at last', what is really going on?",
             "opts": ["They are hiding how upset they are about Ffion leaving", "They are truly pleased to have the room to themselves",
                      "They want Gethin to come and share the room", "They are tired of Gethin asking about Ffion"],
             "why": "The narrator only 'told myself I was glad', and the last paragraph says the feeling 'was not anger at all': the brave words cover sadness."},
            {"id": "9615522ba9c8", "t": "mcq", "d": "retrieve", "q": "What reason does the narrator give for not seeing the sunset clearly?",
             "opts": ["The wind was making their eyes water", "The sun was shining straight into their eyes",
                      "Spray from the sea had got into their eyes", "Sand was blowing up off the beach"],
             "why": "The narrator says 'something about the wind making my eyes water'."},
            {"id": "10e9dce5c0bf", "t": "mcq", "d": "language", "q": "Why does the writer describe the sea turning from grey to 'a kind of burning copper' at this moment?",
             "opts": ["The sudden colour mirrors the narrator's feelings rising", "It warns the reader that a storm is coming",
                      "It shows that the evening is turning cold", "It explains why the two of them must go home"],
             "why": "Just as the sea flares into a 'burning' colour, the narrator's hidden feelings break through and their eyes fill with tears."},
            {"id": "33f218ff1de8", "t": "mcq", "d": "retrieve", "q": "What does Ffion do that she 'had not done since I was small'?",
             "opts": ["Puts her arm round the narrator's shoulders", "Hands the narrator a flat stone to skim",
                      "Laughs when the narrator's stone sinks", "Asks the narrator to walk to the beach"],
             "why": "The text says 'She just put her arm round my shoulders, which she had not done since I was small'."},
            {"id": "2959b7ecd2e8", "t": "mcq", "d": "infer", "q": "In what way is the thirteen-year-old narrator an unreliable narrator of their own feelings?",
             "opts": ["They say they feel angry and glad, but their actions show sadness", "They invent events on the beach that never happened",
                      "They mix up the order in which things happened", "They pretend to be Ffion when telling the story"],
             "why": "The young narrator claims to be angry and glad, but cannot see through tears and lets Ffion hold them; the older narrator admits it 'was not anger at all'.",
             "no": {"They invent events on the beach that never happened": "Nothing suggests the events are made up; it is the narrator's account of their own feelings that cannot be trusted."}},
            {"id": "3f0245915f07", "t": "mcq", "d": "structure", "q": "How does the final paragraph change the way the reader understands the story?",
             "opts": ["The older narrator reveals the 'anger' was really love and loss", "It shows that the narrator still blames Ffion for leaving",
                      "It reveals that Ffion never went to university after all", "It shows the narrator now refuses to skim stones"],
             "why": "Moving to the present, the narrator looks back and understands that the anger was the pain of someone they love moving on.",
             "no": {"It shows the narrator now refuses to skim stones": "The narrator says 'I still try to skim a stone'."}},
        ],
    },
    {
        "key": "RD9.09",
        "year": 9,
        "strand": "Information",
        "title": "Rivers of ice",
        "nc": "Read and understand information texts: follow an explanation of a process and recognise how a writer uses examples",
        "text": "A glacier is a river of ice, and like a river it is always moving, though usually far too slowly to see. It begins high in the mountains or near the poles, where more snow falls in winter than melts in summer. Year after year the snow piles up, and the weight of the new layers presses the older ones beneath into dense, hard ice. When the ice becomes thick enough, it begins to flow downhill under its own weight, grinding the rock beneath it and carrying stones and boulders along with it.\n\n"
                "Glaciers have shaped much of the landscape we know. The deep U-shaped valleys of the Lake District and the Scottish Highlands were carved by glaciers during the last ice age, and many of the scattered boulders that farmers there have cleared from their fields were carried and dropped by ice thousands of years ago.\n\n"
                "A glacier's health depends on a balance. At its upper end, new snow adds ice; at its lower end, or snout, ice melts away. If the two are equal, the glacier stays roughly the same size. If melting wins, the glacier shrinks and its snout retreats up the valley. Today, across most of the world, melting is winning. Scientists measuring glaciers from the Alps to the Andes and the Himalayas have recorded them losing ice as the climate warms, and photographs of the same valleys taken a century apart show bare rock where there was once thick ice.\n\n"
                "This matters far beyond the mountains. Millions of people depend on rivers fed partly by glacier meltwater, especially in Asia and South America, where it keeps rivers flowing through the dry seasons. In the short term, faster melting can mean more water and a greater risk of floods; in the long term, as the glaciers shrink, there may be far less. Melting glaciers also add water to the oceans, which contributes to rising sea levels.\n\n"
                "There is another, less obvious problem. Clean ice and snow are bright, and they reflect much of the sunlight that falls on them back into space. When they melt, they expose darker rock or water, which absorbs more of the sun's heat. That warms the area further, which melts more ice: a cycle that feeds itself.\n\n"
                "In Switzerland, workers have even covered parts of the Rhône Glacier with huge white blankets in summer, to reflect sunlight and slow the melting near a popular ice cave that tourists visit. It is an inventive idea, but it can protect only a tiny patch. The scientists who study glaciers agree that the only lasting way to save them is to slow the warming of the climate itself.",
        "qs": [
            {"id": "8d670938ec54", "t": "mcq", "d": "language", "q": "The writer opens by calling a glacier 'a river of ice'. Why is this comparison useful?",
             "opts": ["It shows that a glacier flows downhill, only slowly", "It shows that glaciers are mostly liquid water",
                      "It shows that glaciers always end in the sea", "It shows that glaciers move fast and are dangerous"],
             "why": "The writer explains the comparison straight away: 'like a river it is always moving', though 'far too slowly to see'."},
            {"id": "6a3c1cfbb103", "t": "order", "d": "sequence", "q": "Put these stages in the order in which a glacier forms, according to the first paragraph.",
             "items": ["More snow falls in winter than melts in summer", "The snow piles up year after year",
                       "The weight presses older layers into hard ice", "The thick ice starts to flow downhill"],
             "why": "The first paragraph explains the process in this order: extra snow, piling up, pressing into ice, then flowing once it is thick enough."},
            {"id": "09101c73b90c", "t": "mcq", "d": "retrieve", "q": "Which places does the second paragraph give as examples of valleys carved by glaciers?",
             "opts": ["The Lake District and the Scottish Highlands", "The Alps and the Andes",
                      "Asia and South America", "Switzerland and the Himalayas"],
             "why": "The second paragraph names the U-shaped valleys 'of the Lake District and the Scottish Highlands'.",
             "no": {"The Alps and the Andes": "These come in the third paragraph, as places where scientists measure glaciers losing ice."}},
            {"id": "87071dd9bd1b", "t": "text", "d": "vocab", "q": "Find and copy the word in the third paragraph that names the lower end of a glacier.",
             "a": ["snout", "the snout", "its snout", "a snout"],
             "why": "The third paragraph says 'at its lower end, or snout, ice melts away'."},
            {"id": "0c4836755096", "t": "mcq", "d": "infer", "q": "Why could melting glaciers bring 'more water' at first but 'far less' later?",
             "opts": ["Ice stored over centuries runs off until little is left", "Rain will replace all the meltwater in time",
                      "Floods will wash the riverbeds away completely", "People will choose to use less water in future"],
             "why": "Faster melting releases ice built up over many years, so rivers swell for a while; once the glacier has shrunk, there is less ice left to feed them."},
            {"id": "49fb39728d51", "t": "mcq", "d": "retrieve", "q": "What is the 'cycle that feeds itself' described in the fifth paragraph?",
             "opts": ["Melting uncovers dark ground, which warms and melts more ice", "Snow falls, melts and falls again every single year",
                      "Rivers fill the oceans, which then make more snow", "White blankets reflect sunlight, which cools the glacier"],
             "why": "Bright ice reflects sunlight; when it melts, darker rock or water absorbs more heat, which melts more ice, and so on."},
            {"id": "37de6684a425", "t": "mcq", "d": "purpose", "q": "Why does the writer describe the blankets on the Rhône Glacier near the end?",
             "opts": ["To show a clever idea that cannot solve the real problem", "To persuade readers to visit the ice cave",
                      "To prove that the glaciers can be saved by covering them", "To explain how the Rhône Glacier was first formed"],
             "why": "The writer calls the blankets 'an inventive idea' but says they protect 'only a tiny patch'; the lasting answer is to slow the warming of the climate.",
             "no": {"To prove that the glaciers can be saved by covering them": "The writer says the blankets protect 'only a tiny patch'."}},
        ],
    },
    {
        "key": "RD9.10",
        "year": 9,
        "strand": "Persuasive writing",
        "title": "The person who steps forward",
        "nc": "Know how a speech persuades: direct address, rhetorical questions, anecdote, emotive language and answering counter-arguments",
        "text": "Good morning, everyone. My name is Amara, I'm in Year 10, and I want to start by asking you a question. If the person sitting next to you collapsed right now and stopped breathing, would you know what to do?\n\n"
                "Be honest. Most of us would freeze. Last spring, I would have frozen too.\n\n"
                "In April, my uncle Kwame went to watch my cousin play football on a Sunday morning. He is fifty-two, he goes running, and nobody thought for a moment that anything was wrong with his heart. In the second half, he stood up to cheer a goal and fell to the ground. His heart had stopped.\n\n"
                "Here is the part I want you to remember. A woman on the touchline, a parent from the other team whom none of us had ever met, ran over, knelt beside him and started chest compressions. Someone else rang 999. A third person remembered that the sports club had a defibrillator on the wall by the changing rooms, and ran to fetch it. By the time the ambulance arrived, my uncle's heart was beating again. Today he is back at work, and last week he beat me at table tennis, which I am still not happy about.\n\n"
                "The doctors told us something I have never forgotten: every minute without help makes it less likely that a person will survive. When the heart stops, waiting for an ambulance is not enough. What happens in those first few minutes, before the professionals arrive, depends on ordinary people. It depends on people like you.\n\n"
                "So I am asking for two things. First, that our school buys a defibrillator and puts it where everyone can see it, by the main entrance. Second, that every pupil, in every year, has a short, practical CPR session once a year, on a real training dummy, not just a slide in a lesson.\n\n"
                "Some of you will say: we're only teenagers; that's a job for adults. I understand. But the woman who saved my uncle was not a doctor or a nurse. She had done one short course at her workplace, years ago. Others will say that defibrillators are complicated and expensive. In fact, a modern defibrillator talks you through every step, and it will not give a shock unless one is needed. As for the cost, our parents' association raised more than that last year for new curtains in the hall. Which matters more?\n\n"
                "We learn so many things in this school that we hope we will use one day. This is one we hope we never need. But if the day comes, I want every one of us to be the person who steps forward, not the person who freezes.\n\n"
                "Thank you.",
        "qs": [
            {"id": "648a4e7de7bf", "t": "mcq", "d": "language", "q": "Why does Amara open her speech with a question to the audience?",
             "opts": ["To make each listener imagine facing that moment", "To count how many pupils already know first aid",
                      "To check that the audience is paying attention", "To admit that she still would not know what to do"],
             "why": "'The person sitting next to you' puts every listener in the situation, so they feel the problem before she explains it.",
             "no": {"To admit that she still would not know what to do": "She says she would have frozen 'last spring', before her uncle collapsed, not now."}},
            {"id": "7f5fd84c62a7", "t": "mcq", "d": "vocab", "q": "The woman who helped was standing 'on the touchline'. What is the touchline?",
             "opts": ["The line along the side of a pitch", "The queue for the club's café",
                      "The line players stand on to start", "The seats behind the goal"],
             "why": "She was a parent watching the football match, so she was standing at the side of the pitch, by the touchline."},
            {"id": "24184187840c", "t": "text", "d": "retrieve", "q": "Where was the sports club's defibrillator kept? Find and copy the two words that name the place it hung beside.",
             "a": ["changing rooms", "the changing rooms", "by the changing rooms", "on the wall by the changing rooms", "changing room", "the changing room", "by the changing room"],
             "why": "Amara says the club had 'a defibrillator on the wall by the changing rooms'."},
            {"id": "208e5839c1ea", "t": "mcq", "d": "infer", "q": "Why does Amara mention that her uncle 'beat me at table tennis'?",
             "opts": ["To show, with a touch of humour, that he has fully recovered", "To prove that table tennis is good for the heart",
                      "To complain that her uncle never lets her win", "To suggest that he is still not completely well"],
             "why": "Being well enough to win at table tennis shows he is back to normal, and her joke about not being happy lightens the mood after a frightening story."},
            {"id": "4c16a22cfb64", "t": "mcq", "d": "retrieve", "q": "What two things does Amara ask the school to do?",
             "opts": ["Buy a defibrillator and give every pupil yearly CPR practice", "Hire a school nurse and start a first-aid club",
                      "Buy a defibrillator and new curtains for the hall", "Show a slide about CPR in every lesson"],
             "why": "She asks for a defibrillator by the main entrance and a practical CPR session for every pupil once a year.",
             "no": {"Show a slide about CPR in every lesson": "She asks for practice on a real training dummy, 'not just a slide in a lesson'."}},
            {"id": "182e703db711", "t": "mcq", "d": "infer", "q": "How does Amara answer the counter-argument that helping in an emergency is 'a job for adults'?",
             "opts": ["She shows that an ordinary person with little training saved a life", "She says that teenagers are stronger than most adults",
                      "She says the defibrillator does all the CPR by itself", "She agrees, and asks pupils to fetch an adult quickly"],
             "why": "She points out that the woman who saved her uncle 'was not a doctor or a nurse' and had done only one short course."},
            {"id": "f131636943c7", "t": "mcq", "d": "purpose", "q": "What is the main purpose of Amara's speech?",
             "opts": ["To persuade the school to train pupils and buy a defibrillator", "To thank the stranger who saved her uncle's life",
                      "To explain to pupils how a defibrillator works", "To describe a football match she watched in April"],
             "why": "The story of her uncle supports her two requests: a defibrillator for the school and CPR practice for every pupil.",
             "no": {"To thank the stranger who saved her uncle's life": "The story of the stranger is there to support her requests to the school."}},
        ],
    },
    {
        "key": "RD9.11",
        "year": 9,
        "strand": "Stories",
        "title": "The shoot by the drain",
        "nc": "Recognise an unreliable narrator in dystopian fiction; infer and predict from details in the text",
        "text": "My name is Citizen 4471-B, though my friends, when we are allowed friends, call me Tess. I want to say at the start that I am very happy. Everyone in Sector Nine is very happy. The screens tell us so every morning at six, and the screens have never been wrong.\n\n"
                "My day begins when the light panel above my bed turns from grey to a soft, approved yellow. I have eleven minutes to wash and dress. My clothes are laid out by the wall hatch: the blue overall for Tuesdays, the same as everyone's, which is fair. Breakfast is a square of oat paste and a cup of warm water flavoured with something the label calls Citrus Option. I do not remember what a citrus is, but I am sure it was not important.\n\n"
                "At 6.40 I join the walking line to the Training Hall. We walk in pairs, at the approved pace, and we do not talk, because talking slows the line. I do not mind. Silence is restful. That is what the screens say, and I have found it to be true, mostly.\n\n"
                "This morning, something happened which I should probably not mention.\n\n"
                "Between Block Twelve and the Training Hall there is a strip of concrete where nothing grows. Today, in a crack near the drain, there was a small green shoot with two leaves, no bigger than my fingernail. I noticed it because I nearly stepped on it. The boy beside me, 4502-C, noticed it too. He slowed down. I slowed down. For perhaps two seconds, the line bent around us like a stream around a stone.\n\n"
                "Nobody said anything. Of course nobody did. We are very happy, and a weed is not news.\n\n"
                "But at lunch, when I was meant to be eating my second square of paste, I found that I had drawn the shoot on the back of my hand in pen. Two leaves. One stem. I do not know why I did it. I washed it off before the afternoon check, scrubbing until the skin went red, and nobody saw.\n\n"
                "Tomorrow is Wednesday, which means the grey overall. The walking line will leave at 6.40, as always. I have worked out that if I walk on the left of the pair instead of the right, I will pass right beside the crack near the drain, and I will be able to see whether the shoot is still there.\n\n"
                "This is not important. I just want to know. I am very happy.",
        "qs": [
            {"id": "b622eed70a40", "t": "mcq", "d": "retrieve", "q": "According to the first paragraph, how do the people of Sector Nine know that they are happy?",
             "opts": ["The screens tell them every morning", "Their friends remind them each day",
                      "They are taught it at the Training Hall", "They write it in a diary every night"],
             "why": "The first paragraph says 'The screens tell us so every morning at six'."},
            {"id": "b4a574abe62a", "t": "mcq", "d": "vocab", "q": "What does 'approved' mean in 'We walk in pairs, at the approved pace'?",
             "opts": ["Officially allowed by those in charge", "Very slow and tiring to keep up",
                      "Pleasant and relaxed for everyone", "Chosen by each walker for themselves"],
             "why": "Something approved has been officially accepted; in Sector Nine even the walking speed is set by those in charge, like the 'approved yellow' light."},
            {"id": "80256c2a27c9", "t": "mcq", "d": "infer", "q": "'I do not remember what a citrus is, but I am sure it was not important.' What does this suggest?",
             "opts": ["Real fruit has vanished and Tess has learned not to care", "Tess has never liked the taste of fruit",
                      "Citrus Option is a new and exciting drink", "Tess often forgets what she learns in lessons"],
             "why": "The drink is named after a fruit Tess no longer remembers, and she brushes it aside as unimportant: she has been taught not to question what is missing."},
            {"id": "3c1bb938b4a9", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you how big the shoot was, compared with part of Tess's body.",
             "s": "Today, in a crack near the drain, there was a small green shoot with two leaves, no bigger than my [fingernail].",
             "why": "The shoot was 'no bigger than my fingernail'."},
            {"id": "7789813d4bdd", "t": "mcq", "d": "retrieve", "q": "What does Tess do with her drawing of the shoot before the afternoon check?",
             "opts": ["She scrubs it off her hand until the skin goes red", "She shows it to the boy who walks beside her",
                      "She hides it under the sleeve of her overall", "She copies it carefully onto a piece of paper"],
             "why": "She says 'I washed it off before the afternoon check, scrubbing until the skin went red'."},
            {"id": "8aee9aa9d963", "t": "mcq", "d": "infer", "q": "Tess keeps saying 'I am very happy'. Why is she an unreliable narrator?",
             "opts": ["Her actions show a longing that she will not admit", "She lies to the reader about finding the shoot",
                      "She forgets which day of the week it is", "She is telling the story of someone else"],
             "why": "She draws the shoot, hides it and plans to see it again, yet insists 'This is not important': what she does tells us more than what she says.",
             "no": {"She lies to the reader about finding the shoot": "She tells us about the shoot openly; it is her claims about her own feelings that we cannot trust."}},
            {"id": "5eab73dfba1e", "t": "mcq", "d": "predict", "q": "What is Tess most likely to do tomorrow morning?",
             "opts": ["Walk on the left of her pair to check on the shoot", "Report the shoot to the people who run the screens",
                      "Stay in her room instead of joining the line", "Pull up the shoot so that nobody else sees it"],
             "why": "She has 'worked out' that walking on the left will take her past the crack, so she can see whether the shoot is still there."},
        ],
    },
    {
        "key": "RD9.12",
        "year": 9,
        "strand": "Information",
        "title": "The real price of a cheap T-shirt",
        "nc": "Read a magazine feature critically: follow an explanation, compare viewpoints and identify the writer's overall view",
        "text": "£4 for a T-shirt. £12 for a pair of jeans. £15 for a dress you saw on your phone last night and can wear to a party this weekend. For many of us, clothes have never been so cheap or so quick to buy. But as economists like to say, there is no such thing as a free lunch, and there may be no such thing as a £4 T-shirt either.\n\n"
                "Maisie, 15, from Bristol, is honest about her habits. 'I buy something most weeks,' she says. 'It's so cheap that it doesn't feel like a big decision. If I only wear it twice, it doesn't matter.' She is far from alone. 'Fast fashion' is the name for a business model built on speed: designs are copied from catwalks or social media, made in huge quantities, and in the shops within weeks. Some companies now add new styles almost every day.\n\n"
                "How can the prices be so low? Part of the answer is scale. A factory making a million identical shirts can buy fabric more cheaply and run its machines more efficiently than one making a hundred; economists call these savings economies of scale. Another part is wages. Most of the world's clothes are sewn in countries where workers are paid far less than in Britain, and the pressure to keep prices low can mean long hours and poor conditions for the people at the sewing machines.\n\n"
                "Then there are the costs that never appear on the label at all. Growing cotton needs huge amounts of water. Polyester, the most common fabric in cheap clothing, is a kind of plastic made from oil, and it sheds tiny fibres when washed that can end up in rivers and the sea. When clothes are thrown away after a few wears, many end up buried in landfill or burned. Economists have a name for costs like these, which are paid by someone other than the buyer and the seller: external costs. The planet, and people far away, pick up the bill.\n\n"
                "Yusuf has run a small clothes-repair shop in Leeds for twenty years, and he has noticed a change. 'People used to bring me coats to mend, good trousers to take in,' he says. 'Then a new one started costing less than the repair. Why would you fix it?' But lately, he adds, more young customers have been coming in, asking him to save a favourite jacket or alter something they found second-hand.\n\n"
                "So what can one shopper do? Buy less, and choose things you will wear many times. Look after what you own. Try charity shops, swaps with friends, or a needle and thread. None of this will change the industry overnight. But in economics, demand shapes supply, and every purchase sends a small signal about the kind of fashion we want.",
        "qs": [
            {"id": "bea6dfb41f5f", "t": "mcq", "d": "retrieve", "q": "According to the second paragraph, how does 'fast fashion' work?",
             "opts": ["Designs are copied, made in bulk and in shops within weeks", "Clothes are made slowly by hand to last for years",
                      "Old clothes are collected and sold on second-hand", "Shoppers design their own clothes on their phones"],
             "why": "The second paragraph says designs 'are copied from catwalks or social media, made in huge quantities, and in the shops within weeks'."},
            {"id": "eee76e1d8b11", "t": "mcq", "d": "infer", "q": "What do Maisie's words suggest about the effect of very low prices?",
             "opts": ["They make buying clothes feel careless and unimportant", "They mean she can rarely afford to buy clothes",
                      "They make her regret everything she buys", "They mean she buys clothes only for parties"],
             "why": "She says it 'doesn't feel like a big decision' and it 'doesn't matter' if she wears something only twice: cheapness makes buying feel trivial."},
            {"id": "53cb12713f27", "t": "text", "d": "vocab", "q": "Find and copy the term economists use for the savings a factory makes by producing in huge quantities.",
             "a": ["economies of scale"],
             "why": "The third paragraph says 'economists call these savings economies of scale'."},
            {"id": "342bfe2f7df3", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you what the plastic in polyester is made from.",
             "s": "Polyester, the most common fabric in cheap clothing, is a kind of plastic made from [oil], and it sheds tiny fibres when washed that can end up in rivers and the sea.",
             "why": "The text says polyester 'is a kind of plastic made from oil'."},
            {"id": "4a2bf66662ae", "t": "mcq", "d": "retrieve", "q": "What are 'external costs', as the fourth paragraph explains them?",
             "opts": ["Costs paid by someone other than the buyer and seller", "Costs of shipping clothes in from abroad",
                      "Extra charges that shops add on at the till", "Costs of running a factory's sewing machines"],
             "why": "The fourth paragraph defines them as costs 'paid by someone other than the buyer and the seller', such as the planet and people far away."},
            {"id": "a7c79b16d62a", "t": "mcq", "d": "compare", "q": "How has Yusuf's trade changed over time, according to him?",
             "opts": ["Repairs fell away, but young people have lately started returning", "Repairs grew steadily, and young people now do them at home",
                      "Young customers have always been the main part of his trade", "He has stopped repairing clothes and now sells new ones"],
             "why": "He says people stopped mending once a new item cost less than the repair, but 'lately' more young customers have been coming in."},
            {"id": "6214205ee04d", "t": "mcq", "d": "summarise", "q": "Which statement best sums up the writer's view in this feature?",
             "opts": ["Cheap clothes have hidden costs, and shoppers can choose differently", "Fast fashion is good because everyone can afford new clothes",
                      "Only the largest companies can ever change the fashion industry", "Repairing clothes is now always cheaper than buying new ones"],
             "why": "The feature explains the costs that 'never appear on the label', then ends with what 'one shopper' can do: buy less, look after clothes, try second-hand.",
             "no": {"Repairing clothes is now always cheaper than buying new ones": "Yusuf says the opposite: a new item can cost less than the repair."}},
        ],
    },
]
