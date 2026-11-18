"""Reading comprehension, Year 9, second set (keys RD9.13-RD9.24).

Twelve more original passages, written by hand, continuing the bridge from KS3 reading to GCSE English
Language begun in reading_y9.py, on different topics and with different names and settings. As there, the
questions ask what the GCSE papers ask (what you learn from a section, how the writer uses language, how the
text is structured, a reader's evaluation of a statement, viewpoints compared), as mcq, tap, find-and-copy and
order questions, never essays. Terms met: personification, metaphor, contrast, flashback, inverted pyramid,
stage directions, refrain, anecdote, rhetorical question, counter-argument.

* RD9.13 a 19th-century-style arrival in a northern steel town (story)
* RD9.14 the Great Stink of 1858 and London's sewers (information)
* RD9.15 a holiday diary from a tree nursery in the hills of Kenya (diary)
* RD9.16 Marie Curie (biography)
* RD9.17 'The Shout', a poem about a volunteer lifeboat crew (poem)
* RD9.18 how earthquakes and tsunamis happen (explanation)
* RD9.19 an opinion article: why everyone should learn another language (persuasive)
* RD9.20 a cello audition in Leeds, told with a flashback (story)
* RD9.21 a local news report: pupils survey a Norfolk sea wall (news report)
* RD9.22 a scene at a bus stop about a lost wallet (play script)
* RD9.23 coral reefs (information)
* RD9.24 a night under the desert sky in northern Chile (story)

Non-fiction facts are limited to well-established ones taught in English schools; uncertain numbers are
left out. The news report is about an invented village. To be reviewed line by line by a second reader before
release.
"""

SKILLS = [
    {
        "key": "RD9.13",
        "year": 9,
        "strand": "Stories",
        "title": "Arrival at Brackenfield",
        "nc": "Know how language, including figurative language and vocabulary choice, presents meaning in fiction from the 19th century",
        "text": "I had been told, before I left the quiet village where I was born, that Brackenfield was a town of smoke, and I had pictured something like the drift from a cottage chimney on a still evening. I had not pictured this. As the train came round the last curve of the valley, the whole sky ahead of us seemed to darken, as though a great hand had been laid across it, and beneath that hand rose the chimneys: thirty, forty, I could not count them, each one breathing out its own black plume into the common gloom.\n\n"
                "The station was a roar of steam and voices. Porters shouted, trucks rattled over the stones, and a whistle shrieked so close beside me that I dropped my umbrella and very nearly my courage with it. I stood on the platform with my box at my feet and the letter from the school committee in my glove, and I confess that for a moment I wished myself back among the hedges and the larks.\n\n"
                "It was then that I heard the works. I had expected noise, but not a noise like this: a deep and endless thudding of great hammers, felt through the soles of the feet as much as heard, as if the town had a heart of iron and it was beating far too fast. Out in the street, a crowd of women and girls was coming off the early shift at the cutlery workshops, their clogs clattering on the cobbles, their shawls drawn over their heads against the drizzle. Their faces were streaked with the black dust of the polishing wheels, and their hands, I noticed, were rough and red; yet they talked and laughed as they walked, and called to one another across the road in an accent so broad that I understood perhaps one word in three.\n\n"
                "One of them, a girl of fourteen or fifteen with a cough she did not seem to notice, saw me staring helplessly at my directions. Without a word of introduction she took one handle of my box, nodded at me to take the other, and led me up a steep street to the very door of the school. When I tried to thank her, she only laughed and said something I took to mean that I would soon learn the way myself.\n\n"
                "I have lived in Brackenfield now for three months. The smoke is no lighter and the hammers are no quieter, and I still cannot always follow what my pupils say. But I have stopped wishing for the hedges. A town where a tired girl will carry a stranger's box up a hill at the end of a ten-hour shift is not, I have come to think, so dark a place as it first appears.",
        "qs": [
            {"id": "f6b4d66e152c", "t": "mcq", "d": "retrieve", "q": "Before arriving, what had the narrator imagined the smoke of Brackenfield would be like?",
             "opts": ["Like the drift from a cottage chimney", "Like a great hand laid across the sky",
                      "Like the steam from the railway engine", "Like the drizzle coming down the valley"],
             "why": "The first sentence says the narrator 'pictured something like the drift from a cottage chimney on a still evening'.",
             "no": {"Like a great hand laid across the sky": "That is what the narrator actually sees from the train, not what was pictured before setting off."}},
            {"id": "448d23bc178f", "t": "tap", "d": "language", "q": "Tap the word that makes the chimneys seem like living creatures.",
             "s": "As the train came round the last curve of the valley, the whole sky ahead of us seemed to darken, as though a great hand had been laid across it, and beneath that hand rose the chimneys: thirty, forty, I could not count them, each one [breathing] out its own black plume into the common gloom.",
             "why": "Chimneys cannot breathe: 'breathing' personifies them, as if each one were alive and puffing out smoke."},
            {"id": "7e295310988b", "t": "mcq", "d": "infer", "q": "What does the narrator mean by dropping the umbrella 'and very nearly my courage with it'?",
             "opts": ["The noise and bustle almost made the narrator lose their nerve", "The narrator nearly dropped the committee's letter as well",
                      "The narrator was cross with the porters for shouting", "The narrator felt brave enough to face anything"],
             "why": "Dropping one's courage is a figure of speech: the shriek of the whistle and the roar of the station nearly made the narrator lose heart, and wish to be back home.",
             "no": {"The narrator nearly dropped the committee's letter as well": "The letter stays safe 'in my glove'; it is courage, not a real object, that the narrator nearly loses."}},
            {"id": "bac7d6e0f3ef", "t": "mcq", "d": "language", "q": "The narrator says the town seemed to have 'a heart of iron' that 'was beating far too fast'. What does this image suggest?",
             "opts": ["The town is driven by its machines and never rests", "The townspeople are hard and unkind",
                      "The works are about to break down", "The narrator's own heart is racing with joy"],
             "why": "The heartbeat is the endless thudding of the hammers: like a heart that beats too fast, the town's machines work without pause.",
             "no": {"The townspeople are hard and unkind": "'Heart of iron' could mean that in other texts, but here it describes the thudding of the hammers, and the people turn out to be kind."}},
            {"id": "76c784d46ce3", "t": "mcq", "d": "compare", "q": "In the third paragraph, how do the women workers' looks compare with their behaviour?",
             "opts": ["They look worn out, yet they are cheerful and lively", "They look cheerful, yet they are silent and unfriendly",
                      "They look well dressed, yet they speak roughly", "They look young, yet they walk slowly and sadly"],
             "why": "Their faces are streaked with black dust and their hands rough and red, 'yet they talked and laughed as they walked'."},
            {"id": "e663c28501c1", "t": "text", "d": "retrieve", "q": "Find and copy the phrase in the last paragraph that tells you how long the girl had just worked.",
             "a": ["a ten-hour shift", "ten-hour shift", "ten hour shift", "a ten hour shift", "ten-hour", "ten hours"],
             "why": "The last paragraph says the girl carried the box 'at the end of a ten-hour shift'."},
            {"id": "4e0468c8d7bb", "t": "mcq", "d": "structure", "q": "How does the narrator's view of Brackenfield change from the beginning of the passage to the end?",
             "opts": ["From dismay at the town to respect for its people", "From excitement about the town to disappointment in it",
                      "From dislike of the smoke to enjoyment of it", "From fear of the works to a wish to work in them"],
             "why": "At first the narrator wishes to be back home; by the end the narrator has 'stopped wishing for the hedges' because of the kindness of people like the girl who carried the box.",
             "no": {"From dislike of the smoke to enjoyment of it": "The narrator says 'The smoke is no lighter': what has changed is the narrator's view of the people, not the smoke."}},
        ],
    },
    {
        "key": "RD9.14",
        "year": 9,
        "strand": "Information",
        "title": "The Great Stink",
        "nc": "Read a wide range of non-fiction critically: summarise and synthesise information, and follow the structure of an explanation",
        "text": "In the first half of the nineteenth century, London grew faster than any city in Britain had grown before. Its population rose year after year, but the way it dealt with human waste hardly changed at all. Much of the sewage from homes and streets ran, through old drains and open ditches, straight into the River Thames. The same river supplied many Londoners with their drinking water.\n\n"
                "The results were deadly. Several times in those decades, the disease cholera swept through the city, killing thousands of people within a few weeks. Most doctors at the time believed that diseases like cholera were spread by 'miasma': foul-smelling, poisonous air rising from rotting rubbish and filth. A doctor called John Snow disagreed. During an outbreak in Soho in 1854, he marked on a map the homes of the people who had died, and found that they clustered around a single water pump in Broad Street. When the pump's handle was removed, the cases in that area fell away. Snow argued that cholera was carried in dirty water, not in the air, but few people were convinced.\n\n"
                "What finally forced a change was not an argument but a smell. The summer of 1858 was unusually hot, and the low, sluggish Thames, thick with sewage, began to stink so badly that the newspapers named the season the Great Stink. The Houses of Parliament stand on the river bank, and the politicians inside could no longer ignore the problem: curtains were soaked in chemicals in an attempt to block the stench. Within weeks, a law was passed to pay for a new system of sewers.\n\n"
                "The man chosen to build it was the engineer Joseph Bazalgette. His plan was bold. Huge new sewers, lined with millions of bricks, would run alongside the river and catch the waste before it reached the water, carrying it east and releasing it far downstream of the city. Some of these sewers were hidden inside new embankments built along the Thames, which also gave London new roads and riverside gardens. Bazalgette is said to have made his pipes far wider than his calculations required, in case the city kept growing. It did, and the extra space has been needed ever since.\n\n"
                "The new system was a remarkable success. Once it was complete, cholera never again struck London on the old scale, and the river slowly became cleaner. There is an irony in the story, though. The sewers were built largely to get rid of a smell, because many people still believed in miasma. They saved lives for the reason John Snow had given: they kept sewage out of the water that people drank. More than a century and a half later, much of Bazalgette's network is still in use beneath the streets of London.",
        "qs": [
            {"id": "9b8ae1c7a66d", "t": "mcq", "d": "retrieve", "q": "According to the first paragraph, why was it so dangerous that sewage ran into the Thames?",
             "opts": ["Many Londoners drank water from the same river", "The river flooded the streets every summer",
                      "Ships could no longer sail up the river", "The sewage killed the fish in the river"],
             "why": "The first paragraph ends: 'The same river supplied many Londoners with their drinking water.'"},
            {"id": "fa9c3fc9d0b6", "t": "text", "d": "vocab", "q": "Find and copy the word, in inverted commas in the second paragraph, for the bad air that most doctors blamed for disease.",
             "a": ["miasma", "'miasma'"],
             "why": "Most doctors believed diseases were spread by 'miasma': foul-smelling, poisonous air."},
            {"id": "456ec5910ad1", "t": "mcq", "d": "infer", "q": "Why does the writer include the detail that cases fell when the pump's handle was removed?",
             "opts": ["It is evidence that the illness came from the water", "It shows that Snow repaired the broken pump",
                      "It proves that the air in Soho had become cleaner", "It explains why people refused to believe Snow"],
             "why": "Once nobody could take water from that pump, the cases there fell away: strong evidence for Snow's idea that cholera was carried in water.",
             "no": {"It explains why people refused to believe Snow": "The text says few were convinced, but the pump detail is the evidence that he was right, not a reason for doubting him."}},
            {"id": "f579167a3630", "t": "tap", "d": "vocab", "q": "Tap the word in this sentence that describes the slow movement of the river.",
             "s": "The summer of 1858 was unusually hot, and the low, [sluggish] Thames, thick with sewage, began to stink so badly that the newspapers named the season the Great Stink.",
             "why": "Sluggish means slow-moving and heavy, like a slug: a slow river could not carry the sewage away."},
            {"id": "ef21550e0af9", "t": "order", "d": "sequence", "q": "Put these events in the order they happened, according to the passage.",
             "items": ["John Snow maps the deaths around a pump in Soho", "A hot summer makes the Thames stink",
                       "A law is passed to pay for new sewers", "Bazalgette's sewers carry waste far downstream"],
             "why": "Snow's map was in 1854; the Great Stink was in 1858; the law followed within weeks; then Bazalgette built the sewers."},
            {"id": "5cb4d08ca41d", "t": "mcq", "d": "retrieve", "q": "What other benefits, besides hiding sewers, did the new embankments bring, according to the fourth paragraph?",
             "opts": ["New roads and riverside gardens", "Cleaner drinking water pumps",
                      "Wider bridges across the Thames", "New homes for London's workers"],
             "why": "The fourth paragraph says the embankments 'also gave London new roads and riverside gardens'."},
            {"id": "4add9ee0d17c", "t": "mcq", "d": "summarise", "q": "What is the 'irony' that the writer points out in the last paragraph?",
             "opts": ["The sewers were built to remove a smell but worked by keeping water clean", "The sewers were built too large and were never fully used",
                      "John Snow designed the sewers but Bazalgette got the credit", "The sewers made the smell worse before they made it better"],
             "why": "People wanted to get rid of the smell (because they believed in miasma), but the sewers saved lives for Snow's reason: they kept sewage out of drinking water.",
             "no": {"The sewers were built too large and were never fully used": "The fourth paragraph says the extra space 'has been needed ever since'."}},
        ],
    },
    {
        "key": "RD9.15",
        "year": 9,
        "strand": "Letters and diaries",
        "title": "Seedlings: a holiday diary",
        "nc": "Read a wide range of non-fiction, including diaries; recognise how a writer's viewpoint and tone change over a text",
        "text": "Saturday\nArrived at Shosho's house in the hills above Nyeri after seven hours on the road. Mum says I will love it. I say there is one bar of signal, and only if you stand on the water tank. Shosho is my grandmother. She is seventy-three and she was already out in her garden when we pulled up, in a woolly hat and wellington boots, as if it were the most normal thing in the world to be digging at five o'clock in the evening. Two weeks of this. I have brought four books. I may have to read them twice.\n\n"
                "Monday\nShosho runs a tree nursery with six other women from the village. I thought this would mean a shop. It means a long shed with a roof of green netting and hundreds and hundreds of seedlings in black plastic sleeves, all in rows, like a classroom of very small, very quiet pupils. My job today was watering. It took all morning. Shosho checked every row afterwards and showed me where I had missed. I did not say anything, but I was annoyed.\n\n"
                "Wednesday\nToday we carried two hundred seedlings to the school down the hill, where the pupils are planting a line of trees along the edge of their playing field. Shosho says the field used to wash away in the long rains, and that the roots will hold the soil together. A boy called Kamau, who is about my age, showed me how to dig the hole twice as wide as the sleeve and press the earth down with your heel. He has planted, he says, over a hundred trees. I have now planted eleven. I am counting.\n\n"
                "Friday\nIt rained in the night, properly, drumming on the iron roof so loudly that I could not sleep. In the morning I went straight down to the nursery without being asked. Two rows of the youngest seedlings had been flattened, and I spent an hour standing them up and pressing the soil back round them. Shosho came and watched and said nothing for a long time. Then she said, 'Now you know why I check every row.' I wanted to be annoyed again, but I could not quite manage it.\n\n"
                "Sunday\nSix days left. I have read one book. Kamau says the trees we planted on Wednesday will be taller than both of us in about five years, and that I will have to come back and see them. Shosho says I can take a seedling home to Nairobi if I promise to look after it. I have chosen one already. It is in a black plastic sleeve by my bed, and I water it every morning, and I have not missed it once.",
        "qs": [
            {"id": "3e92f5ad6cfe", "t": "mcq", "d": "infer", "q": "How does the writer feel about the visit in the Saturday entry?",
             "opts": ["Unenthusiastic and expecting to be bored", "Excited to see Shosho's nursery",
                      "Worried that Shosho is unwell", "Glad to be away from the phone"],
             "why": "The writer complains about the single bar of signal, counts the weeks ('Two weeks of this') and jokes about having to read the books twice.",
             "no": {"Glad to be away from the phone": "The writer is annoyed that there is almost no signal, not glad of it."}},
            {"id": "d5529915c525", "t": "tap", "d": "language", "q": "The writer uses a simile to describe the seedlings. Tap the word for the people the seedlings are compared to.",
             "s": "It means a long shed with a roof of green netting and hundreds and hundreds of seedlings in black plastic sleeves, all in rows, like a classroom of very small, very quiet [pupils].",
             "why": "The seedlings in their rows are compared to pupils in a classroom: small, quiet and lined up neatly."},
            {"id": "1865e13efb98", "t": "mcq", "d": "retrieve", "q": "Why are the pupils planting trees along the edge of their playing field?",
             "opts": ["The roots will stop the soil washing away in the rains", "The trees will give shade during the hot season",
                      "The trees will keep animals off the field", "The school wants to sell the fruit"],
             "why": "Shosho says the field 'used to wash away in the long rains' and that the roots will hold the soil together."},
            {"id": "ae25ea5a70a9", "t": "mcq", "d": "infer", "q": "What does 'I have now planted eleven. I am counting.' suggest about the writer?",
             "opts": ["The writer has started to care about the work and wants to do well", "The writer thinks planting trees is a waste of time",
                      "The writer is checking that Kamau is telling the truth", "The writer is keeping count in order to stop at twelve"],
             "why": "After hearing that Kamau has planted over a hundred, the writer proudly keeps track of their own number: the writer is becoming interested and a little competitive.",
             "no": {"The writer is checking that Kamau is telling the truth": "The writer is counting their own trees, not his."}},
            {"id": "7180379f3ff6", "t": "text", "d": "retrieve", "q": "Find and copy the three words from the Friday entry that show the writer went to the nursery by choice.",
             "a": ["without being asked"],
             "why": "On Friday the writer 'went straight down to the nursery without being asked'."},
            {"id": "ff510eb4ecb1", "t": "mcq", "d": "compare", "q": "Compare how the writer reacts to Shosho checking the writer's work on Monday and on Friday.",
             "opts": ["Annoyed on Monday; on Friday, understanding why", "Grateful on Monday; on Friday, annoyed",
                      "Arguing with Shosho on both days", "Pleased with the praise on both days"],
             "why": "On Monday the writer 'was annoyed'; on Friday, after seeing the flattened seedlings, the writer 'could not quite manage' to be annoyed, now seeing why every row is checked."},
            {"id": "8eddee08cea9", "t": "mcq", "d": "structure", "q": "How does the last entry link back to the first?",
             "opts": ["The books are still mostly unread, showing how the writer's interests have changed", "The writer is still standing on the water tank to find a signal",
                      "The writer is still complaining that the visit is too long", "The writer leaves for Nairobi a week after arriving"],
             "why": "On Saturday the writer feared having to read the four books twice; by Sunday only one has been read, because the trees have taken over the writer's days.",
             "no": {"The writer leaves for Nairobi a week after arriving": "The last entry says 'Six days left': the writer is not leaving yet."}},
        ],
    },
    {
        "key": "RD9.16",
        "year": 9,
        "strand": "Biography",
        "title": "Marie Curie: a life in the laboratory",
        "nc": "Read biography critically: identify the writer's viewpoint and how facts are selected and organised",
        "text": "Maria Skłodowska was born in Warsaw in 1867, at a time when Poland was ruled by Russia. She was a brilliant pupil, but there was a problem: women were not allowed to study at the university in Warsaw. For a time she went to secret classes, held in private homes, where young Poles taught one another the subjects the authorities would rather they did not learn. Then she made a deal with her older sister, Bronisława. Maria would work as a governess and send money to help Bronisława study medicine in Paris; afterwards, Bronisława would help her in return.\n\n"
                "The deal took years to complete, but in 1891 Maria finally arrived in Paris and enrolled at the Sorbonne, calling herself Marie. She lived in a tiny attic room, so cold in winter that she sometimes slept with all her clothes piled on top of her, and she studied so hard that she occasionally forgot to eat. She graduated in physics at the top of her class, and soon afterwards took a second degree in mathematics. In 1895 she married Pierre Curie, a French physicist who shared her passion for research.\n\n"
                "Marie chose to study the strange rays given off by the element uranium, rays that the scientist Henri Becquerel had recently discovered. She found that the strength of the rays depended only on the amount of uranium, which suggested that they came from inside the atoms themselves. She called this property radioactivity. Working with Pierre in a leaky, badly heated shed, she processed tonnes of rock by hand, stirring huge pots with an iron rod almost as tall as she was, and in 1898 the couple announced two new elements. One of them she named polonium, after the country of her birth; the other was radium.\n\n"
                "In 1903 the Curies and Becquerel shared the Nobel Prize in Physics. Marie was the first woman ever to win a Nobel Prize. Three years later, Pierre was killed in a street accident in Paris. Marie was devastated, but she took over his post and became the first woman to teach at the Sorbonne as a professor. In 1911 she won a second Nobel Prize, this time in chemistry, becoming the first person to win two.\n\n"
                "During the First World War, Curie helped to equip vehicles with X-ray machines so that surgeons near the front line could find bullets and broken bones, and she drove some of them herself. She died in 1934 of an illness that was very probably caused by years of working with radioactive materials, whose dangers nobody at first understood. Her notebooks are still so radioactive that they are kept in lead-lined boxes. They are a reminder of both the price she paid and the extraordinary determination with which she worked.",
        "qs": [
            {"id": "8b2926876b10", "t": "mcq", "d": "retrieve", "q": "Why could Maria not go to university in Warsaw?",
             "opts": ["Women were not allowed to study there", "Her family could not afford the fees",
                      "The university had been closed by Russia", "She had already left for Paris"],
             "why": "The first paragraph says 'women were not allowed to study at the university in Warsaw'."},
            {"id": "2e9df69ba2f2", "t": "mcq", "d": "infer", "q": "What does the 'deal' between the two sisters show about them?",
             "opts": ["They were willing to make sacrifices to help each other", "They did not trust each other with money",
                      "They both wanted to become doctors in Paris", "They were forced by their parents to work"],
             "why": "Maria worked for years as a governess to pay for Bronisława's studies, trusting that her sister would help her later: each was ready to give something up for the other.",
             "no": {"They both wanted to become doctors in Paris": "Only Bronisława studied medicine; Maria studied physics and mathematics."}},
            {"id": "aa15532154c6", "t": "tap", "d": "retrieve", "q": "Tap the two words that tell you which subjects Marie took degrees in.",
             "s": "She graduated in [physics] at the top of her class, and soon afterwards took a second degree in [mathematics].",
             "why": "She graduated first in physics and then took a second degree in mathematics."},
            {"id": "1f3006e6282d", "t": "text", "d": "vocab", "q": "Find and copy the word Marie Curie invented for the property of giving off rays from inside atoms.",
             "a": ["radioactivity"],
             "why": "The third paragraph says 'She called this property radioactivity.'"},
            {"id": "5cf7879f2b1d", "t": "mcq", "d": "language", "q": "Why does the writer mention the 'leaky, badly heated shed' and the iron rod 'almost as tall as she was'?",
             "opts": ["To show how hard the conditions of her great work were", "To explain why the experiments kept failing",
                      "To suggest that Pierre did most of the heavy work", "To show that the Curies had plenty of money"],
             "why": "These details show the discovery was made by hard physical labour in poor conditions, which makes her achievement more impressive.",
             "no": {"To explain why the experiments kept failing": "The experiments succeeded: 'in 1898 the couple announced two new elements'."}},
            {"id": "ee6dff262015", "t": "mcq", "d": "retrieve", "q": "Which of these 'firsts' does the passage say Marie Curie achieved in 1911?",
             "opts": ["The first person to win two Nobel Prizes", "The first woman to win a Nobel Prize",
                      "The first woman to teach at the Sorbonne", "The first person to discover uranium"],
             "why": "In 1911 she won the chemistry prize, 'becoming the first person to win two'. The first woman Nobel winner was in 1903; the Sorbonne post came after 1906.",
             "no": {"The first woman to win a Nobel Prize": "That happened in 1903, with the physics prize."}},
            {"id": "6edd660c897a", "t": "mcq", "d": "purpose", "q": "What overall impression of Marie Curie does the writer want the reader to have?",
             "opts": ["A determined scientist who overcame great obstacles", "A lucky scientist who made one chance discovery",
                      "A careless scientist who ignored known dangers", "A shy scientist who let others take the credit"],
             "why": "The writer stresses the obstacles (no university, poverty, the shed, grief) and ends on her 'extraordinary determination'.",
             "no": {"A careless scientist who ignored known dangers": "The text says the dangers were something 'nobody at first understood'."}},
        ],
    },
    {
        "key": "RD9.17",
        "year": 9,
        "strand": "Poems",
        "title": "The Shout",
        "nc": "Read poetry critically: how imagery, repetition and the structure of a poem present meaning",
        "text": "At ten past two the pager shrieks\non the chair beside Lena's bed,\nand before it has finished its second cry\nshe is pulling a jumper over her head.\n\n"
                "She does not wake the house. Her boots\nare waiting where she left them by the door,\nlaced loose for this. Outside, the street\nis black and wet and empty, and the roar\n\n"
                "she heard in her sleep without hearing\nis louder here: the sea, throwing its weight\nagainst the harbour wall, again, again,\nlike a fist on a locked gate.\n\n"
                "Down the hill the station lights are burning.\nOthers are running too: Tom from the bakery,\nstill dusted white; Mrs Hale, who teaches maths;\nyoung Kofi from the garage, half awake.\n\n"
                "No one says much. They have done this before.\nEach one has a locker, and a lifejacket, and a place,\nand in four minutes, maybe five,\nthe boat goes down the slipway into the dark\nwith a sound like a held breath let go.\n\n"
                "Out past the wall the sea is not a sea.\nIt is a hill, then a hole, then a hill,\nand the boat climbs and falls and climbs,\nand the spray comes over the bow like thrown gravel.\nSomewhere out there is a fishing boat\nwith its engine dead and two men aboard,\nand the sea does not care.\n\n"
                "They search for an hour. The radio crackles.\nThe searchlight swings its long white arm\nacross the water, finding nothing, nothing,\nand then, at last, a flash of orange:\na lifejacket, a waving hand, a face.\n\n"
                "Then hands on ropes, on rails, on sleeves,\nthe long pull up and over the side,\nthe two men shaking under foil blankets,\none of them saying thank you, thank you,\nas if he had forgotten every other word.\n\n"
                "Coming home, the sea is still a hill and a hole.\nIt has not changed its mind. It never does.\nBut the boat is heavier now, by two men,\nand lighter in every other way.\n\n"
                "At six the crew walk back up through the town.\nTom opens the bakery. Mrs Hale goes home to shower\nbefore the first bell. Kofi falls asleep in his car.\nAnd Lena climbs the stair and lies down in her clothes,\nthe pager on the chair beside her,\nquiet, for now.",
        "qs": [
            {"id": "4b086b9472c1", "t": "mcq", "d": "retrieve", "q": "What has Lena done to make sure she can leave the house quickly?",
             "opts": ["Left her boots loosely laced by the door", "Slept in her lifejacket and boots",
                      "Kept her car keys beside the pager", "Asked her family to wake her up"],
             "why": "The second verse says her boots are 'waiting where she left them by the door, laced loose for this'.",
             "no": {"Asked her family to wake her up": "'She does not wake the house': she goes without disturbing anyone."}},
            {"id": "af9c095ec5c8", "t": "tap", "d": "language", "q": "Tap the word for the thing the sea is compared to as it crashes against the harbour wall.",
             "s": "the sea, throwing its weight against the harbour wall, again, again, like a [fist] on a locked gate.",
             "why": "The simile compares the sea to a fist hammering on a locked gate: the waves strike the wall over and over, hard and angry."},
            {"id": "63fdfb198313", "t": "mcq", "d": "infer", "q": "What does the fourth verse, about Tom, Mrs Hale and Kofi, tell you about the lifeboat crew?",
             "opts": ["They are ordinary local people who volunteer", "They are paid sailors who live at the station",
                      "They are all members of Lena's family", "They have never been to sea before"],
             "why": "They have everyday jobs in the town (a baker, a maths teacher, a garage worker) and come running at night: they are volunteers.",
             "no": {"They have never been to sea before": "The next verse says 'They have done this before.'"}},
            {"id": "c39bb8725719", "t": "mcq", "d": "language", "q": "The poet writes that the sea 'is a hill, then a hole, then a hill'. What does this metaphor suggest?",
             "opts": ["The waves are so big that the boat rises and drops steeply", "The sea is calm and flat once the boat is past the wall",
                      "The boat has run aground on a hill near the shore", "The crew can see the land rising behind them"],
             "why": "Hills and holes are the huge waves and the deep troughs between them; the next line says the boat 'climbs and falls and climbs'."},
            {"id": "ea7ff9654333", "t": "text", "d": "retrieve", "q": "Find and copy the colour that the crew finally see in the water.",
             "a": ["orange", "a flash of orange", "flash of orange"],
             "why": "After an hour of finding nothing, they see 'a flash of orange': a lifejacket."},
            {"id": "0bd76e43a53a", "t": "mcq", "d": "infer", "q": "What does the poet mean by the boat being 'heavier now, by two men, / and lighter in every other way'?",
             "opts": ["The crew's worry has lifted now the men are safe", "The boat has used up most of its fuel",
                      "The two fishermen have thrown their nets away", "The sea has become calmer on the way home"],
             "why": "The boat carries two more people, but the crew feel relief: the weight of fear and searching has gone.",
             "no": {"The sea has become calmer on the way home": "The poem says the sea 'has not changed its mind': it is still 'a hill and a hole'."}},
            {"id": "af61d015a91f", "t": "mcq", "d": "structure", "q": "How does the ending of the poem link back to its beginning?",
             "opts": ["It returns to Lena's bed and the pager on the chair", "It repeats the time the pager went off",
                      "It returns to the roar of the sea against the wall", "It ends, as it began, with the crew running downhill"],
             "why": "The poem opens with the pager shrieking on the chair beside Lena's bed and ends with her lying down beside it, 'quiet, for now': a cyclical structure.",
             "no": {"It repeats the time the pager went off": "The poem begins at ten past two and ends at six: the time is not repeated."}},
        ],
    },
    {
        "key": "RD9.18",
        "year": 9,
        "strand": "Explanations",
        "title": "When the ground moves",
        "nc": "Read explanations critically: follow a chain of cause and effect and the way technical vocabulary is introduced",
        "text": "The ground beneath our feet feels solid and still, but it is neither. The Earth's outer layer, the crust, is broken into enormous pieces called tectonic plates, which fit together rather like the cracked shell of a boiled egg. Heat from deep inside the planet keeps these plates moving very slowly, by a few centimetres a year, roughly the speed at which your fingernails grow.\n\n"
                "Most earthquakes happen where two plates meet. At these boundaries the plates may be pulling apart, pushing together or sliding past each other, but they rarely move smoothly. Their rough edges catch and lock, while the forces pushing them keep on building. For years, sometimes for centuries, nothing seems to happen. Then the rock suddenly gives way, the plates jerk into a new position, and the stored energy is released in waves that travel out through the ground. These seismic waves are what we feel as an earthquake.\n\n"
                "The point underground where the rock first breaks is called the focus. The place on the surface directly above it is the epicentre, and this is usually where the shaking is strongest. Scientists record the waves with instruments called seismometers, and measure the size of an earthquake on a magnitude scale. The scale is not like a ruler: each step up means a much bigger earthquake than the one before, so a magnitude 7 earthquake releases far more energy than a magnitude 6.\n\n"
                "When an earthquake happens under the sea, it can cause a second disaster. If the seabed is suddenly lifted, the whole column of water above it is pushed upwards, and waves spread out across the ocean. This is a tsunami. In deep water the waves are surprisingly low, and a ship might not notice one passing, but they travel extremely fast, as fast as a jet aircraft. As they reach shallow water near a coast, they slow down and pile up into walls of water that can flood far inland. Often the first warning is strange: the sea draws back from the beach, leaving fish stranded on the sand. Anyone who sees this should move to high ground at once. In December 2004, a tsunami caused by an earthquake off the coast of Indonesia struck countries all around the Indian Ocean, and many of the people who died had no warning at all.\n\n"
                "Earthquakes cannot yet be predicted, but their harm can be reduced. In countries such as Japan, buildings are designed to sway rather than crack, children practise what to do in school, and warning systems detect the first waves and send alerts to phones and trains. Ocean sensors now watch for tsunamis too. The ground will keep moving; the aim is to be ready when it does.",
        "qs": [
            {"id": "f4f9ff6e3b8c", "t": "mcq", "d": "language", "q": "Why does the writer compare the Earth's crust to 'the cracked shell of a boiled egg'?",
             "opts": ["It is a thin outer layer broken into pieces that fit together", "It is soft on the outside and hard in the middle",
                      "It is so fragile that it could shatter at any moment", "It is smooth and has no gaps in it at all"],
             "why": "A cracked eggshell is a thin covering split into pieces that still fit together, like the tectonic plates of the crust."},
            {"id": "da53a62c2f7a", "t": "text", "d": "retrieve", "q": "Find and copy the part of the body whose growth is used to show how fast the plates move.",
             "a": ["fingernails", "your fingernails", "fingernail", "nails"],
             "why": "The plates move 'roughly the speed at which your fingernails grow'."},
            {"id": "4f670d6b730b", "t": "order", "d": "sequence", "q": "Put these stages of an earthquake in order, as the second paragraph explains them.",
             "items": ["The edges of two plates catch and lock", "The forces on the plates build up for years",
                       "The rock suddenly gives way", "Seismic waves travel out through the ground"],
             "why": "The plates lock, pressure builds, the rock gives way, and the released energy travels as seismic waves."},
            {"id": "74ddd3952a62", "t": "mcq", "d": "retrieve", "q": "According to the third paragraph, what is the epicentre of an earthquake?",
             "opts": ["The place on the surface directly above the focus", "The point underground where the rock first breaks",
                      "The instrument that records the seismic waves", "The edge where two tectonic plates meet"],
             "why": "The third paragraph says the epicentre is 'the place on the surface directly above' the focus.",
             "no": {"The point underground where the rock first breaks": "That is the focus; the epicentre is on the surface above it."}},
            {"id": "7a8d9f777263", "t": "mcq", "d": "infer", "q": "Why does the writer say the magnitude scale 'is not like a ruler'?",
             "opts": ["Each step on it is much bigger than the one before", "It can only be read by trained scientists",
                      "It works only for earthquakes under the sea", "It has no highest or lowest number"],
             "why": "On a ruler every step is the same size; on the magnitude scale 'each step up means a much bigger earthquake than the one before'."},
            {"id": "b9aac0eee73f", "t": "mcq", "d": "retrieve", "q": "According to the fourth paragraph, what often happens just before a tsunami reaches the shore?",
             "opts": ["The sea draws back from the beach", "Ships out at sea are thrown about",
                      "The waves become low and fast", "Alerts are sent to every phone"],
             "why": "The fourth paragraph says 'the sea draws back from the beach, leaving fish stranded on the sand'.",
             "no": {"The waves become low and fast": "That is how a tsunami travels in deep water, far from the coast."}},
            {"id": "02d5ee17a0de", "t": "mcq", "d": "structure", "q": "How does the last paragraph change the direction of the passage?",
             "opts": ["It turns from how earthquakes happen to how people prepare", "It turns from tsunamis to the history of Japan",
                      "It turns from facts to a story about one survivor", "It turns from the sea back to the cracked eggshell"],
             "why": "After explaining causes and effects, the writer ends with how harm can be reduced: building design, school drills and warning systems."},
        ],
    },
    {
        "key": "RD9.19",
        "year": 9,
        "strand": "Persuasive writing",
        "title": "Say it in their words",
        "nc": "Read persuasive writing critically: recognise the techniques a writer uses, including anecdote, rhetorical questions and the handling of counter-arguments",
        "text": "Two summers ago, in a small market town in Portugal, I watched an elderly stallholder trying to explain to a British tourist that the peaches on the front of her stall were not for sale. They were for show; the ones to buy were in the boxes behind. The tourist spoke more and more slowly, and more and more loudly, in English. The stallholder spoke more and more quickly in Portuguese. Both of them grew red in the face. Then a girl of about twelve, the tourist's daughter, stepped forward and said, in careful school Portuguese, 'Excuse me, which ones can we buy?' The stallholder's whole face changed. Within a minute the two of them were laughing, and the family walked away with a bag of peaches and a free melon.\n\n"
                "That is what a second language does. It does not just help you to buy fruit. It turns a stranger into a person.\n\n"
                "Many people in Britain believe there is no point in learning another language, because 'everyone speaks English'. It is true that English is widely spoken, and that a traveller can often get by without anything else. But getting by is not the same as understanding. If you only ever speak to people in your language, you only ever meet them halfway, and usually less than halfway. You hear what they can manage to say, not what they really mean.\n\n"
                "There are practical reasons too. Employers value people who can work with partners and customers abroad, and a language on your CV tells them that you are patient, that you can cope with being confused, and that you are willing to keep trying. Learning a language also changes the way you understand your own. You notice how English builds a sentence only when you have seen another language build it differently.\n\n"
                "Some say that translation apps will soon make all this unnecessary. Why spend years learning verbs when your phone can do it in a second? Apps are useful, and I would not be without one. But try making a friend through a screen held between your faces. Try telling a joke. An app can swap words for other words; it cannot make the stallholder's face change the way that girl did.\n\n"
                "Nobody needs to become fluent overnight. Ten words, learned properly and used with a smile, are worth more than a thousand typed into a phone. So pick a language, any language, and start. Learn to say hello, please and thank you. Learn to ask a question. You may be surprised how many doors those few words open.",
        "qs": [
            {"id": "db2818cd113f", "t": "mcq", "d": "retrieve", "q": "What was the stallholder trying to explain to the tourist?",
             "opts": ["The peaches at the front were only for show", "The peaches had all been sold that morning",
                      "The melons were cheaper than the peaches", "The market was about to close for the day"],
             "why": "The first paragraph says she was explaining 'that the peaches on the front of her stall were not for sale. They were for show'."},
            {"id": "916edbf24e5b", "t": "mcq", "d": "structure", "q": "Why does the writer begin with the story of the market stall?",
             "opts": ["To show the argument through a real moment readers can picture", "To complain about British tourists abroad",
                      "To advise readers on where to buy fruit in Portugal", "To prove that Portuguese is easy to learn"],
             "why": "The anecdote shows a few words of Portuguese changing an argument into laughter, before the writer explains the point in the second paragraph.",
             "no": {"To complain about British tourists abroad": "The tourist's daughter is the hero of the story; the writer is showing what a language can do, not attacking tourists."}},
            {"id": "1dc33a8d1fb3", "t": "mcq", "d": "vocab", "q": "In the third paragraph, what does 'get by' mean in 'a traveller can often get by without anything else'?",
             "opts": ["Manage well enough to cope", "Travel past without stopping",
                      "Become fluent very quickly", "Avoid speaking to anyone"],
             "why": "To get by is to manage with what you have: here, to cope abroad using English alone.",
             "no": {"Travel past without stopping": "'Get by' can mean squeeze past something, but here it is about coping with only English."}},
            {"id": "9e3559f3055c", "t": "mcq", "d": "infer", "q": "In the third paragraph, what does the writer mean by 'getting by is not the same as understanding'?",
             "opts": ["Managing simple tasks is not the same as really knowing what people mean", "Travellers who cannot speak English will get lost",
                      "Most people abroad pretend not to understand English", "It is impossible to travel without a second language"],
             "why": "The writer says that with English alone 'You hear what they can manage to say, not what they really mean.'",
             "no": {"It is impossible to travel without a second language": "The writer admits 'a traveller can often get by without anything else'."}},
            {"id": "c20e21633cea", "t": "mcq", "d": "retrieve", "q": "According to the fourth paragraph, what does a language on your CV tell employers about you?",
             "opts": ["That you are patient and willing to keep trying", "That you have lived abroad for a long time",
                      "That you will not need a translation app", "That you are good at English grammar"],
             "why": "The fourth paragraph says it tells them 'that you are patient, that you can cope with being confused, and that you are willing to keep trying'."},
            {"id": "0ba3b5818162", "t": "mcq", "d": "purpose", "q": "How does the writer deal with the view that translation apps will make learning languages unnecessary?",
             "opts": ["They admit apps are useful, then show what apps cannot do", "They say apps are useless and should be banned",
                      "They agree completely and change their mind", "They ignore it and move on to talk about jobs"],
             "why": "The writer concedes 'Apps are useful, and I would not be without one', then argues that an app cannot make a friend or tell a joke: a counter-argument answered.",
             "no": {"They say apps are useless and should be banned": "The writer says 'I would not be without one'."}},
            {"id": "566c5127392f", "t": "text", "d": "vocab", "q": "Find and copy the word in the last paragraph that means able to speak a language easily and well.",
             "a": ["fluent"],
             "why": "'Nobody needs to become fluent overnight': fluent means speaking a language easily and well."},
        ],
    },
    {
        "key": "RD9.20",
        "year": 9,
        "strand": "Stories",
        "title": "The audition",
        "nc": "Know how the structure of a story, including a flashback and a shift in focus, is used to interest the reader",
        "text": "The waiting room smelled of floor polish and radiators. Nadia sat on a plastic chair with her cello case standing between her knees like a tall, silent friend, and listened to the boy before her playing through the wall. He was good. He was very good. Every note came out clean and certain, and each one seemed to land on her chest like a small stone.\n\n"
                "She looked at her hands. They were cold, though the room was warm, and her left thumb had started its familiar tremble. On the train from Bradford she had gone through the piece forty times in her head, every bowing, every shift, and now she could not remember how the second page began.\n\n"
                "The first cello she ever played had belonged to the school. It was scratched and patched, with a crack near the tailpiece mended with glue, and it had stood in a cupboard for years before Mr Adeyemi found it. She was eight. She had wanted the violin, because her friend was having violin lessons, but there were no violins left, and so she sat down, sulking, behind this enormous, battered thing. Mr Adeyemi did not hand her the bow. Instead he plucked the lowest string and told her to put her hand flat on the wood. The sound went right through the instrument and into her palm, deep and warm, like a cat purring. 'Listen before you play,' he said. 'Always listen first.' She had not wanted the violin since.\n\n"
                "The music next door stopped. There was a murmur of voices and the scrape of a chair, and then the door opened and the boy came out, holding his case to his chest. He looked pale and rather younger than his playing. 'They're nice,' he said, as he passed her, and she was so surprised that she forgot to answer.\n\n"
                "'Nadia Hussain?' A woman with a clipboard was smiling at her from the doorway.\n\n"
                "The room was larger than she had expected and almost empty: three people behind a table, a music stand, a chair, and a tall window full of grey Leeds sky. Nadia sat, and opened her case, and lifted out the cello. It was her own now, not the school's, but she still found herself checking the place near the tailpiece where the old crack had been.\n\n"
                "She tuned. Then, before she lifted the bow, she plucked the lowest string, very quietly, and felt the sound go into the wood and into her hand. Her thumb was still. The second page, she found, was exactly where she had left it.",
        "qs": [
            {"id": "55d39f27fc3b", "t": "tap", "d": "language", "q": "The writer uses a simile to show how the other boy's playing makes Nadia feel. Tap the noun that each note is compared to.",
             "s": "Every note came out clean and certain, and each one seemed to land on her chest like a small [stone].",
             "why": "Each note lands 'like a small stone': his good playing weighs on her and makes her more anxious."},
            {"id": "f1667e21384b", "t": "mcq", "d": "retrieve", "q": "What has Nadia forgotten while she waits?",
             "opts": ["How the second page of her piece begins", "Which piece she was asked to play",
                      "The name of her first music teacher", "Where she left her cello's bow"],
             "why": "The second paragraph says 'now she could not remember how the second page began'."},
            {"id": "ffd1b4d05c3a", "t": "mcq", "d": "structure", "q": "What does the third paragraph do in the structure of the story?",
             "opts": ["It moves back in time to Nadia's first cello lesson", "It describes what is happening in the audition room",
                      "It jumps forward to the result of the audition", "It tells the story from Mr Adeyemi's point of view"],
             "why": "It is a flashback: 'She was eight.' It interrupts the waiting room scene to tell how she began to play.",
             "no": {"It jumps forward to the result of the audition": "We never learn the result; the third paragraph goes back to when she was eight."}},
            {"id": "1392ac247d55", "t": "mcq", "d": "infer", "q": "How did Nadia feel about the cello at the very start of her first lesson?",
             "opts": ["Disappointed, because she had wanted the violin", "Delighted, because it was so large",
                      "Frightened, because it was cracked", "Proud, because Mr Adeyemi chose her"],
             "why": "She sat down 'sulking', because she had wanted the violin like her friend but none were left.",
             "no": {"Frightened, because it was cracked": "The crack is described, but nothing shows it scared her; she was sulking about the violin."}},
            {"id": "81751cad87ca", "t": "text", "d": "vocab", "q": "Find and copy the adjective just before the word 'thing' in the third paragraph that tells you the school cello was old and knocked about.",
             "a": ["battered"],
             "why": "She sits behind 'this enormous, battered thing': battered means damaged by long use."},
            {"id": "c840550340ef", "t": "mcq", "d": "infer", "q": "Why is Nadia 'so surprised' by what the boy says as he leaves?",
             "opts": ["She expected the judges to be frightening", "She expected him to boast about his playing",
                      "She did not know he had heard her name", "She thought he had failed the audition"],
             "why": "She has been sitting tense and nervous, picturing the audition as an ordeal; being told the judges are 'nice' is the last thing she expects."},
            {"id": "58094370e8b5", "t": "mcq", "d": "structure", "q": "Why does the writer have Nadia pluck the lowest string at the end, before she plays?",
             "opts": ["It links back to Mr Adeyemi's advice and shows she is calm again", "It shows she has forgotten how to use the bow",
                      "It shows the judges asking her to tune the cello", "It is a warning that the old crack has opened"],
             "why": "She does what Mr Adeyemi taught her ('Listen before you play'); straight after, her thumb is still and the second page comes back.",
             "no": {"It is a warning that the old crack has opened": "It is her own cello now; she only checks the place 'where the old crack had been'."}},
        ],
    },
    {
        "key": "RD9.21",
        "year": 9,
        "strand": "News reports",
        "title": "Pupils' survey finds weak spots in sea wall",
        "nc": "Read news reports critically: distinguish fact from opinion and see how a report is structured for its readers",
        "text": "A group of Year 9 pupils from a Norfolk coastal village have discovered three weak sections in the sea wall that protects their homes, and the district council has agreed to repair them before next winter.\n\n"
                "The twenty-four pupils from Wexham High School spent six weeks surveying the two-kilometre wall at Wexham-next-the-Sea as part of a geography project. Working in small groups at low tide, they measured the height of the wall every fifty metres, photographed every crack wider than a pencil, and recorded where the concrete had begun to crumble. They then marked each problem on a large map of the seafront.\n\n"
                "When the map was finished, a pattern stood out. Most of the damage was clustered in three places, all of them where the beach in front of the wall had become lower, leaving the base of the wall exposed to the waves.\n\n"
                "'We honestly thought we'd find a few cracks and that would be it,' said Amara Clarke, 14, who led one of the survey groups. 'When we put everything on the map, you could see it straight away. It was a bit scary, actually, because my nan lives right behind one of the bad bits.'\n\n"
                "The pupils presented their findings to the council's coastal engineers in March. The engineers inspected the three sections the following week and confirmed that all of them needed urgent work.\n\n"
                "'The students' survey was careful, accurate and extremely useful,' said a council spokesperson. 'Our own inspections take place every year, but this level of detail, at every fifty metres, gave us a much clearer picture. We have brought forward repairs to all three sections, and they will be completed before the autumn storms.'\n\n"
                "Not everyone in the village was surprised. Jean Holt, 81, who has lived on the seafront for more than fifty years, said she had been worried about the wall for some time. 'You can hear the waves hitting the bottom of it on a rough night in a way you never used to,' she said. 'It took the youngsters to get anyone to look properly. Good for them.'\n\n"
                "Geography teacher Mr Vikram Patel said the project had shown pupils that what they learned in the classroom could make a real difference. 'They did the hard part themselves, out in all weathers,' he said. 'I just carried the tape measures.'\n\n"
                "The pupils now plan to repeat the survey every year, and have offered to share their method with other schools along the coast.",
        "qs": [
            {"id": "1fce8347570c", "t": "mcq", "d": "structure", "q": "Why does the first paragraph of the report contain the main facts of the whole story?",
             "opts": ["So a reader who stops early still knows what happened", "So the report can end with a surprise twist",
                      "So the pupils' names can be kept until last", "So the reader knows the opinions before the facts"],
             "why": "News reports put the most important facts first (an 'inverted pyramid'): who, what and the result are in the first sentence, with details after."},
            {"id": "af481279ead2", "t": "mcq", "d": "retrieve", "q": "Which of these did the pupils record during their survey, according to the second paragraph?",
             "opts": ["Every crack wider than a pencil", "The height of the waves at high tide",
                      "The age of every house on the seafront", "The number of people using the beach"],
             "why": "They 'photographed every crack wider than a pencil', measured the wall's height and noted crumbling concrete.",
             "no": {"The height of the waves at high tide": "They measured the height of the wall, not the waves, and they worked at low tide."}},
            {"id": "cb40e731c2b0", "t": "mcq", "d": "retrieve", "q": "What did the three damaged sections have in common?",
             "opts": ["The beach in front of them had become lower", "They were the oldest parts of the wall",
                      "They were closest to the pupils' school", "They had been repaired badly before"],
             "why": "The third paragraph says all three were 'where the beach in front of the wall had become lower'."},
            {"id": "197ed31a47bb", "t": "mcq", "d": "infer", "q": "Why did Amara find the results 'a bit scary'?",
             "opts": ["Someone close to her lives behind a weak section", "She was afraid of presenting to the engineers",
                      "She had to work on the wall at night", "She worried the survey contained mistakes"],
             "why": "She says 'my nan lives right behind one of the bad bits': the danger was close to her own family."},
            {"id": "d9078bda4d8e", "t": "text", "d": "vocab", "q": "Find and copy the two words in the sixth paragraph that mean the council moved the repairs to an earlier date.",
             "a": ["brought forward"],
             "why": "The spokesperson says 'We have brought forward repairs': they will happen sooner than planned."},
            {"id": "a30f6b8d67e4", "t": "mcq", "d": "infer", "q": "What does Jean Holt's comment 'It took the youngsters to get anyone to look properly' suggest?",
             "opts": ["She thinks adults had not paid enough attention to the wall", "She thinks the pupils damaged the wall during the survey",
                      "She thinks the council's engineers did a better job", "She thinks young people should not be on the seafront"],
             "why": "She had been worried 'for some time', and says it was the pupils who finally got the wall looked at properly: until then nobody had.",
             "no": {"She thinks the council's engineers did a better job": "She praises the pupils ('Good for them'), not the engineers."}},
            {"id": "b78989d6654b", "t": "mcq", "d": "infer", "q": "When Mr Patel says 'I just carried the tape measures', what is he suggesting?",
             "opts": ["The pupils deserve the credit for the work", "He did not want the pupils to use the tape measures",
                      "He was the only one who knew how to measure", "The survey was easier than people think"],
             "why": "He jokingly plays down his own part to praise the pupils: 'They did the hard part themselves.'"},
        ],
    },
    {
        "key": "RD9.22",
        "year": 9,
        "strand": "Play scripts",
        "title": "The number 14",
        "nc": "Read and understand a play script: how dialogue and stage directions reveal character and build tension",
        "text": "(A bus shelter on a wet evening in Cardiff. JESS, 14, sits on the narrow bench, hood up. OMAR, 14, comes in out of the rain, shaking his umbrella. He stops, bends down, and picks up a brown leather wallet from under the bench.)\n"
                "OMAR: Jess. Someone's dropped this.\n"
                "JESS: (pulling out one earphone) Dropped what?\n"
                "OMAR: (opening it) A wallet. There's money in it. (He counts.) Sixty pounds. And cards, and a bus pass, and... a letter from the hospital.\n"
                "JESS: (sitting up) Sixty? Let me see.\n"
                "OMAR: (holding it out of reach) No. Hang on.\n"
                "JESS: Whoever dropped it has gone. The bus before ours left ten minutes ago. Finders keepers, Omar. That's how it works.\n"
                "OMAR: Is it? Who says?\n"
                "JESS: Everyone says. If you hand it in, someone at the bus station will just keep it themselves. At least this way somebody nice gets it. (She grins.) Us.\n"
                "OMAR: (turning the wallet over) There's a photo in here as well. A little boy on a beach, holding up a bucket.\n"
                "JESS: Somebody's grandson, probably. Doesn't change anything.\n"
                "OMAR: Sixty pounds is a lot of money to lose.\n"
                "JESS: Sixty pounds is a lot of money to find. Think what we could do with it. The cinema, chips afterwards, the train to the seaside on Saturday. We'd still have some left over.\n"
                "OMAR: (not looking up) And whoever lost it would still have none.\n"
                "JESS: (rolling her eyes) Go on, then. Read the letter, if you're going to.\n"
                "OMAR: (reading the letter, slowly) It's an appointment. Tomorrow, nine o'clock, at the eye clinic. Mrs Gwen Pritchard. There's an address on Clive Street.\n"
                "JESS: So?\n"
                "OMAR: So her bus pass is in here. How's she going to get to the hospital without it? She's probably at home right now turning out all her pockets.\n"
                "JESS: (after a pause, more quietly) You don't know that.\n"
                "OMAR: I know I'd be. (He shuts the wallet.) Clive Street's two roads away. I'm taking it round.\n"
                "JESS: In this? You'll get soaked.\n"
                "OMAR: (holding up his umbrella) I won't.\n"
                "(JESS looks at him for a long moment. Then she pulls her other earphone out and stands up.)\n"
                "JESS: Fine. But I'm only coming so you don't get lost.\n"
                "OMAR: (smiling) Course you are.\n"
                "(They step out into the rain together, OMAR holding the umbrella over them both. The lights of the empty shelter flicker.)",
        "qs": [
            {"id": "f2e030333689", "t": "mcq", "d": "retrieve", "q": "Where does Omar find the wallet?",
             "opts": ["Under the bench in the bus shelter", "On the seat of the last bus",
                      "In a puddle outside the shelter", "In the pocket of his umbrella"],
             "why": "The opening stage direction says he 'picks up a brown leather wallet from under the bench'."},
            {"id": "7606f5267bed", "t": "mcq", "d": "structure", "q": "What is the main job of the opening stage direction, in brackets?",
             "opts": ["To set the scene and show what happens first", "To give Omar's thoughts about the wallet",
                      "To tell the audience how the scene will end", "To explain why Jess wants to keep the money"],
             "why": "Stage directions are not spoken: this one sets the scene (a wet bus shelter in Cardiff), introduces the characters and shows Omar finding the wallet."},
            {"id": "d7264ce60883", "t": "tap", "d": "retrieve", "q": "Tap the phrase Jess uses to argue that whoever finds something can keep it. Tap both words.",
             "s": "[Finders] [keepers], Omar.",
             "why": "'Finders keepers' is a saying meaning that whoever finds something can keep it."},
            {"id": "71c878e9c9d2", "t": "mcq", "d": "infer", "q": "What makes Omar decide that the wallet must go back to its owner tonight?",
             "opts": ["He realises she needs her bus pass for a hospital appointment", "He is afraid that Jess will take the money",
                      "He thinks he will get a reward for returning it", "He knows Mrs Pritchard from his school"],
             "why": "He reads the letter, sees the appointment is tomorrow at nine and asks, 'How's she going to get to the hospital without it?'",
             "no": {"He thinks he will get a reward for returning it": "Omar never mentions a reward; his reason is the owner's appointment."}},
            {"id": "adbb0e592040", "t": "mcq", "d": "infer", "q": "What does Jess's line '(after a pause, more quietly) You don't know that' suggest?",
             "opts": ["She is beginning to feel uncomfortable about keeping the wallet", "She is angry that Omar will not share the money",
                      "She thinks Omar has read the letter wrongly", "She has stopped listening to Omar"],
             "why": "The pause and the quieter voice show her confidence fading: Omar's picture of the owner searching her pockets has made her think.",
             "no": {"She is angry that Omar will not share the money": "An angry reply would be louder; she speaks 'more quietly' after a pause."}},
            {"id": "bc007c4a7ef2", "t": "text", "d": "retrieve", "q": "Find and copy the name of the street where the owner of the wallet lives.",
             "a": ["Clive Street", "Clive"],
             "why": "Omar reads 'There's an address on Clive Street.'"},
            {"id": "88b37790f5f9", "t": "mcq", "d": "infer", "q": "When Jess says 'I'm only coming so you don't get lost', what does Omar's reply 'Course you are' show?",
             "opts": ["He knows she really wants to help but will not admit it", "He believes he would get lost without her",
                      "He is annoyed that she is coming with him", "He thinks she still wants to keep the money"],
             "why": "Clive Street is only 'two roads away', so her excuse is weak; Omar's smile and 'Course you are' show he sees that she has changed her mind."},
        ],
    },
    {
        "key": "RD9.23",
        "year": 9,
        "strand": "Information",
        "title": "Cities under the sea: coral reefs",
        "nc": "Read a wide range of non-fiction critically: summarise and synthesise information, and recognise how a writer moves from explanation to concern",
        "text": "From the deck of a boat, a coral reef can look like a patch of coloured rock lying just beneath the waves. It is nothing of the kind. A reef is built, and is still being built, by living animals, most of them smaller than a fingernail.\n\n"
                "These animals are called coral polyps. They are distant relatives of jellyfish and sea anemones: each one is a soft, tube-shaped body with a ring of tentacles around its mouth. A polyp cannot build a reef on its own, but it does something remarkable. It takes minerals from the seawater and uses them to make a hard cup of limestone beneath its body. Polyps live packed together in colonies of thousands, and when they die their stony skeletons remain, and new polyps grow on top of them. Layer upon layer, over thousands of years, the skeletons build up into reefs large enough to be seen from an aeroplane. The largest of all, the Great Barrier Reef off the north-east coast of Australia, stretches for a vast distance along the shore.\n\n"
                "Most reef-building corals depend on a partnership. Living inside the polyps' soft tissues are tiny algae, far too small to see. Like plants, the algae use sunlight to make food, and they share much of it with the coral. In return, the coral gives them shelter. The algae also give many corals their bright colours. Because the algae need light, reef-building corals grow only in shallow, clear water, and most need the warmth of tropical seas.\n\n"
                "A healthy reef is crowded with life. Fish of every shape and colour shelter among its branches, along with crabs, shrimps, sea snails, octopuses and turtles. Reefs cover only a tiny part of the ocean floor, yet they are home to a huge share of all the different kinds of sea creature, which is why they are sometimes called the rainforests of the sea. They matter to people, too. They break the force of waves before they reach the shore, protecting coasts from storms, and millions of people depend on reef fish for food.\n\n"
                "Today, many reefs are in trouble. When the sea stays too warm for too long, the corals become stressed and push out the algae living inside them. Without the algae, the coral loses its colour and its main supply of food, and turns ghostly white, as its skeleton shows through the clear tissue. This is called coral bleaching. A bleached coral is not yet dead, and if the water cools in time, the algae can return. If it does not, the coral starves.\n\n"
                "Warming seas are the greatest threat, but pollution and overfishing harm reefs too. Around the world, scientists and local communities are protecting reefs from damage, and some are even growing small pieces of coral in underwater nurseries and planting them back on damaged reefs. The animals that built these cities have survived for a very long time. Whether they continue to do so depends, in large part, on us.",
        "qs": [
            {"id": "4f1a5bf05bd9", "t": "mcq", "d": "structure", "q": "Why does the writer begin by saying a reef can look 'like a patch of coloured rock'?",
             "opts": ["To set up a mistaken idea and then correct it", "To explain how reefs are made from rock",
                      "To describe what a diver sees underwater", "To show that reefs are dangerous to boats"],
             "why": "The next sentence is 'It is nothing of the kind': the writer starts with a common mistake, then surprises the reader with the truth that reefs are built by animals.",
             "no": {"To explain how reefs are made from rock": "The writer says the opposite: a reef is 'nothing of the kind', but is built by living animals."}},
            {"id": "ff335ee7759b", "t": "mcq", "d": "retrieve", "q": "According to the second paragraph, what does a coral polyp make beneath its body?",
             "opts": ["A hard cup of limestone", "A ring of tentacles",
                      "A shelter for tiny algae", "A layer of coloured sand"],
             "why": "The second paragraph says a polyp 'uses them to make a hard cup of limestone beneath its body'.",
             "no": {"A ring of tentacles": "The tentacles are around its mouth, part of its soft body; what it makes beneath its body is a cup of limestone."}},
            {"id": "33abf02aae98", "t": "order", "d": "sequence", "q": "Put these stages in the order in which a reef is built, according to the second paragraph.",
             "items": ["Polyps take minerals from the seawater", "Each polyp makes a stony cup beneath its body",
                       "The polyps die and their skeletons remain", "New polyps grow on top of the old skeletons"],
             "why": "Polyps take minerals, build limestone cups, die leaving skeletons, and new polyps grow on top, layer upon layer."},
            {"id": "fb59bb404444", "t": "mcq", "d": "retrieve", "q": "Why do reef-building corals grow only in shallow, clear water?",
             "opts": ["The algae inside them need sunlight to make food", "The polyps cannot swim in deep water",
                      "The waves are too strong further out", "Fish cannot reach them in deep water"],
             "why": "The third paragraph says 'Because the algae need light, reef-building corals grow only in shallow, clear water': deep or cloudy water would block the sunlight."},
            {"id": "68659356a915", "t": "text", "d": "retrieve", "q": "Find and copy the phrase in the fourth paragraph that reefs are sometimes called.",
             "a": ["rainforests of the sea", "the rainforests of the sea", "the rainforest of the sea", "rainforest of the sea"],
             "why": "The fourth paragraph says reefs 'are sometimes called the rainforests of the sea' because so many kinds of creature live there."},
            {"id": "a51e3f6a021d", "t": "tap", "d": "language", "q": "Tap the word the writer puts before 'white' to make the bleached coral sound lifeless.",
             "s": "Without the algae, the coral loses its colour and its main supply of food, and turns [ghostly] white, as its skeleton shows through the clear tissue.",
             "why": "'Ghostly' white suggests something pale and lifeless, like something no longer alive: the coral has lost the algae that fed and coloured it."},
            {"id": "7bd3b5554147", "t": "mcq", "d": "infer", "q": "A student wrote: 'Once a coral bleaches, it is certain to die.' Which is the best response?",
             "opts": ["No: if the water cools in time, it can recover", "Yes: bleaching means the coral is already dead",
                      "Yes: the algae never come back once they leave", "No: bleaching does not harm coral at all"],
             "why": "The fifth paragraph says 'A bleached coral is not yet dead, and if the water cools in time, the algae can return.'",
             "no": {"No: bleaching does not harm coral at all": "A bleached coral loses its main supply of food and starves if the water stays warm."}},
        ],
    },
    {
        "key": "RD9.24",
        "year": 9,
        "strand": "Stories",
        "title": "Wait for your eyes",
        "nc": "Know how language and structure, including a repeated phrase and a change of setting, present a character's changing feelings",
        "text": "'Wait for your eyes,' Aunt Carmen said, and switched off the torch.\n\n"
                "Ines had not wanted to come. The drive north from the city had taken two days, through a desert so dry and empty that after the first morning she had stopped looking out of the window. There were no trees, no fields, no animals, only stones and dust and a road that went on being the same road for hour after hour. Up at the observatory, where her aunt worked, the air was so thin that climbing a single flight of stairs made Ines's head pound, and she had spent the first afternoon lying on a narrow bed, sipping water and feeling sorry for herself. There was no signal for her phone. There was, as far as she could see, nothing at all.\n\n"
                "Now it was nearly midnight, and they were standing on a slope of loose gravel a few hundred metres from the domes of the telescopes, which were sealed tight against the light. Her aunt had insisted on walking here with only a dim red torch. White light, she said, would spoil their night vision, and it took the eyes a long time to recover.\n\n"
                "At first Ines saw almost nothing: a sprinkling of stars, the shape of the hill, the darker shape of her aunt. She was cold, and cross, and about to say so.\n\n"
                "Then, slowly, the sky began to fill. It was as if someone were turning up a dimmer switch a fraction at a time. Stars appeared behind stars, and more behind those, until there were too many to be separate things at all. Across the middle of the sky ran a pale, cloudy river, with dark patches in it like islands. Ines realised that she had stopped breathing, and made herself start again.\n\n"
                "'The Milky Way,' Aunt Carmen said quietly. 'Our own galaxy, seen from the inside. You can never see it like this in the city. Too much light, too much dust, too much haze.' She pointed to a bright star low over the hills. 'The light from that one left it hundreds of years ago. You are looking at the past.'\n\n"
                "Ines took out her phone, held it up, and then, without taking a picture, put it back in her pocket. The screen would show a black rectangle with a few white dots. It would not show this.\n\n"
                "They stayed until their feet were numb. Walking back, Ines kept stopping to look up, and her aunt let her.\n\n"
                "Two nights later, back in the city, her little brother asked her what was so special about the desert. Ines took him out on to the balcony, where the streetlights turned the sky an orange grey, and switched off the light behind them.\n\n"
                "'Wait for your eyes,' she said.",
        "qs": [
            {"id": "ae9d3600e3fb", "t": "mcq", "d": "infer", "q": "How does Ines feel about the trip in the second paragraph?",
             "opts": ["Bored and unhappy to be there", "Excited to see where her aunt works",
                      "Frightened by the empty desert", "Curious about the telescopes"],
             "why": "She 'had not wanted to come', stopped looking out of the window and spent the afternoon 'feeling sorry for herself'.",
             "no": {"Curious about the telescopes": "Nothing in the second paragraph shows interest: she thinks there is 'nothing at all'."}},
            {"id": "71fa8a17c6df", "t": "mcq", "d": "retrieve", "q": "Why did Ines's head pound at the observatory?",
             "opts": ["The air was so thin up there", "She had been reading in the car",
                      "She had not slept on the long drive", "The sun in the desert was very strong"],
             "why": "The second paragraph says 'the air was so thin that climbing a single flight of stairs made Ines's head pound'."},
            {"id": "440c52cc195f", "t": "mcq", "d": "retrieve", "q": "Why did Aunt Carmen use only a dim red torch?",
             "opts": ["White light would spoil their night vision", "The batteries in the white torch were flat",
                      "Red light would not wake the other scientists", "The telescopes needed red light to work"],
             "why": "The third paragraph says 'White light, she said, would spoil their night vision'."},
            {"id": "a035d60c5e30", "t": "tap", "d": "language", "q": "The writer uses a simile to show how gradually the stars appear. Tap the two words that name the thing being turned up.",
             "s": "It was as if someone were turning up a [dimmer] [switch] a fraction at a time.",
             "why": "A dimmer switch makes a light brighter little by little: the stars do not appear all at once but slowly, more and more of them."},
            {"id": "0fa1fed026fe", "t": "text", "d": "vocab", "q": "Find and copy the word in the eighth paragraph that tells you their feet had lost all feeling from the cold.",
             "a": ["numb"],
             "why": "'They stayed until their feet were numb': numb means unable to feel anything."},
            {"id": "1a0a1a9a77ff", "t": "mcq", "d": "infer", "q": "Why does Ines put her phone away without taking a picture?",
             "opts": ["She realises a photo could never capture what she sees", "Her aunt has told her that phones are not allowed",
                      "The phone has no signal to send the picture", "Her hands are too cold to hold the phone"],
             "why": "She thinks the screen 'would show a black rectangle with a few white dots. It would not show this.'",
             "no": {"The phone has no signal to send the picture": "She has no signal, but that would not stop her taking a photo; her reason is that a picture could not show the sky."}},
            {"id": "ed1fc1f0c76f", "t": "mcq", "d": "structure", "q": "Why does the story end with Ines repeating her aunt's words, 'Wait for your eyes'?",
             "opts": ["To show she has learned to value the patience her aunt taught her", "To show she has forgotten what she saw in the desert",
                      "To show that the city sky is just as full of stars", "To show she is copying her aunt to make fun of her"],
             "why": "The story begins and ends with the same words: Ines, once bored and cross, now passes on her aunt's lesson to her brother.",
             "no": {"To show that the city sky is just as full of stars": "The streetlights turn the city sky 'an orange grey', and Carmen says the Milky Way can never be seen like this in the city."}},
        ],
    },
]
