"""Reading comprehension, Year 7, second set (keys RD7.13-RD7.24).

Twelve more original passages, each written by hand for this bank, 350-550 words, seven questions each,
on topics, names and settings different from reading_y7.py. KS3 English reading (Year 7): inference backed
by evidence, language and its effect (simile, metaphor, personification, word choice), structure (openings,
shifts in focus, endings that link back), the writer's viewpoint and purpose, fact and opinion, and
comparison within a text.

* RD7.13 a cross-country race in Northern Ireland (story)
* RD7.14 Iceland: volcanoes, glaciers and geothermal heat (information)
* RD7.15 a street market setting up at dawn (poem)
* RD7.16 a summer helping a neighbour with his bees (diary)
* RD7.17 Ada Lovelace (biography)
* RD7.18 ospreys return to a Cumbrian nature reserve (news report)
* RD7.19 why we have seasons (explanation)
* RD7.20 every pupil should learn to cook (persuasive article)
* RD7.21 a broken greenhouse pane in Glasgow (play script)
* RD7.22 a mended tea bowl in Kyoto (story)
* RD7.23 Antarctica (information)
* RD7.24 learning to row on the River Trent (story)

Non-fiction uses only well-established facts taught in English schools; the news report is fictional (an
invented reserve, people and quotes) around true background facts. To be reviewed line by line by a second
reader (an English teacher or the bank's reviewer) before release.
"""

SKILLS = [
    {
        "key": "RD7.13",
        "year": 7,
        "strand": "Stories",
        "title": "The last mile",
        "nc": "Make inferences and refer to evidence in the text; know how language and structure present meaning",
        "text": "The start line was a strip of white paint across a field that had been rained on for a week. Niamh Doyle stood in the second row, bouncing on her toes, and watched her breath drift away in the cold air. Two hundred runners from every school in the county were packed behind the line, and only the first ten would be picked for the county team.\n\n"
                "She had trained for this since September. Every morning before school she had run the lane past the farm, up to the cattle grid and back, while her little brother was still asleep. She knew this course by heart: two laps of the playing fields, then out along the river, over the footbridge, and a long climb back up to the finish.\n\n"
                "The starter’s whistle shrieked, and the crowd of runners surged forward. For the first lap Niamh stayed patient, tucked in behind a tall girl in a red vest, letting her take the wind. By the river she had moved up to fourteenth. By the footbridge she was eleventh, and she could hear her heart drumming in her ears.\n\n"
                "Then, on the muddy bank beyond the bridge, the runner in front of her slipped. It was a younger girl from another school, and she went down hard, one leg twisted beneath her. She tried to stand and cried out.\n\n"
                "Runners streamed past on both sides. Niamh felt them go, one, two, five, like coins falling out of a pocket. The nearest marshal was a tiny figure at the top of the hill.\n\n"
                "“Can you walk?” she asked.\n\n"
                "The girl shook her head. Her face was white, and her eyes were full of tears she was trying hard not to let fall. “My ankle,” she whispered.\n\n"
                "Niamh looked up the hill, then back down at the girl. She crouched, pulled the girl’s arm across her shoulders, and together they hobbled up the slope, slipping and stopping, until the marshal came running down to meet them.\n\n"
                "By the time Niamh crossed the finish line, she was twenty-third. She bent over with her hands on her knees, not because she was out of breath, but because she did not want anyone to see her face.\n\n"
                "Mr Haddad, her coach, found her by the tea tent. She expected him to talk about the race, about the places she had thrown away. Instead he handed her a paper cup and said, “The marshal told me what you did.”\n\n"
                "“I didn’t get in the team,” she said.\n\n"
                "“No,” he agreed. “Not this year.” He looked out across the field, where the last runners were still struggling up the hill. “But there are plenty of fast runners in this county, Niamh. There aren’t so many like you.”\n\n"
                "She wrapped her cold hands around the cup. The tea was too sweet and far too hot, and it was the best thing she had ever tasted.",
        "qs": [
            {"id": "45313b01225d", "t": "mcq", "d": "retrieve",
             "q": "What did Niamh need to do to be picked for the county team?",
             "opts": ["Finish among the first ten runners", "Beat the tall girl in the red vest",
                      "Reach the footbridge in eleventh place", "Win the race outright"],
             "no": {"Reach the footbridge in eleventh place": "She was eleventh at the footbridge, but places were decided at the finish, not halfway."},
             "why": "The first paragraph says only the first ten would be picked for the county team."},
            {"id": "d0e1640e3fc4", "t": "text", "d": "retrieve",
             "q": "Find and copy the two words that name the place Niamh ran up to each morning before turning back.",
             "a": ["cattle grid", "the cattle grid", "cattle grids"],
             "why": "The second paragraph: she ran the lane past the farm, “up to the cattle grid and back”."},
            {"id": "8cd81b8c126e", "t": "tap", "d": "language",
             "q": "Tap the verb that describes the sound the starter’s whistle made.",
             "s": "The starter’s whistle [shrieked], and the crowd of runners surged forward.",
             "why": "A shriek is a sudden, high, piercing sound: it makes the start feel sharp and urgent."},
            {"id": "7ce78e75a767", "t": "mcq", "d": "language",
             "q": "“Niamh felt them go, one, two, five, like coins falling out of a pocket.” What does the simile suggest?",
             "opts": ["Places she had worked hard for were slipping away from her",
                      "The other runners were taking places from her on purpose",
                      "The places she lost were small and did not matter to her",
                      "She was losing places slowly, so she had time to catch up"],
             "no": {"She was losing places slowly, so she had time to catch up": "“One, two, five” shows the places going fast, not slowly."},
             "why": "Coins falling from a pocket are something valuable lost without being able to stop it, just like the places she had earned.",
             "why2": "You do not throw coins away on purpose: they slip out. Niamh's places slip away while she stays with the injured girl."},
            {"id": "adf13355b5e5", "t": "mcq", "d": "infer",
             "q": "Why did Niamh bend over with her hands on her knees after the finish?",
             "opts": ["She was upset and wanted to hide it",
                      "She was worn out from helping the girl up the hill",
                      "She had twisted her own ankle on the bank",
                      "She was looking for something she had dropped"],
             "no": {"She was worn out from helping the girl up the hill": "The text says it was “not because she was out of breath”."},
             "why": "She did it “because she did not want anyone to see her face”: she was hiding her disappointment."},
            {"id": "90ce7dea1a41", "t": "mcq", "d": "infer",
             "q": "What does Mr Haddad mean by “There aren’t so many like you”?",
             "opts": ["Kind, unselfish people are harder to find than fast runners",
                      "Very few runners in the county are as fast as Niamh",
                      "Niamh is the only runner from her school this year",
                      "Few runners in the county train on farm lanes as Niamh does"],
             "no": {"Very few runners in the county are as fast as Niamh": "He has just said there are plenty of fast runners: he is praising something else."},
             "why": "He sets “plenty of fast runners” against “not so many like you”, straight after saying “The marshal told me what you did”: he means her kindness in stopping to help.",
             "why2": "Mr Haddad says nothing about her training or her speed; the only thing he has heard about is how she helped the injured girl."},
            {"id": "b30ffd6d9a1a", "t": "mcq", "d": "structure",
             "q": "Why does the story end with the tea being “the best thing she had ever tasted”?",
             "opts": ["It shows her disappointment has eased into quiet pride",
                      "It shows she was very thirsty after the long race",
                      "It shows that Mr Haddad makes very good tea",
                      "It shows she has forgotten all about the race"],
             "no": {"It shows she was very thirsty after the long race": "The tea is “too sweet and far too hot”: it is the moment, not the drink, that makes it the best."},
             "why": "The tea itself is not nice, so its being “the best” shows how much her coach's words meant to her.",
             "why2": "Endings often use a small detail to show a change of feeling: she began by hiding her face and ends glad of what she did."},
        ],
    },
    {
        "key": "RD7.14",
        "year": 7,
        "strand": "Information",
        "title": "Iceland: fire and ice",
        "nc": "Read information texts; retrieve and explain information; understand how a text is organised",
        "text": "Iceland is an island country in the North Atlantic, just south of the Arctic Circle. It is a little smaller than England, yet fewer than half a million people live there, most of them in and around the capital, Reykjavík. Visitors often call it the land of fire and ice, and the name is well earned.\n\n"
                "The fire comes from below. The Earth’s outer layer is broken into huge pieces called tectonic plates, which move very slowly, a few centimetres a year. Iceland sits on top of the Mid-Atlantic Ridge, the line where the North American plate and the Eurasian plate are pulling apart. As they separate, hot molten rock, called magma, rises to fill the gap. This is why Iceland has so many volcanoes, and why one of them erupts every few years. In some places you can walk along a valley where the ground has split between the two plates.\n\n"
                "The ice comes from above. About a tenth of the country is covered by glaciers, great slow rivers of ice built up from centuries of snow. Some of them lie on top of active volcanoes. When a volcano erupts beneath a glacier, the heat can melt an enormous amount of ice in a short time, and the meltwater bursts out in a sudden flood that rushes towards the sea, carrying rocks and blocks of ice with it. Icelanders have their own word for such a flood: a jökulhlaup.\n\n"
                "Eruptions under ice can affect places far away. In 2010, a volcano beneath a glacier called Eyjafjallajökull threw a vast cloud of ash high into the sky. The wind carried it south and east over Europe. Because volcanic ash can badly damage aircraft engines, many airports were closed and thousands of flights were cancelled over several days. A volcano on a small island had grounded planes across a continent.\n\n"
                "Living on top of so much heat has its advantages too. Rainwater and meltwater that seep underground are heated by hot rock, and Icelanders pipe this water into their homes. Most houses are heated this way, and almost all of the country’s electricity comes from renewable sources: geothermal power stations, and rivers fed by the glaciers. The hot water comes out of the tap smelling faintly of eggs, because it contains a gas called hydrogen sulphide. Outdoor swimming pools are filled with this naturally hot water too, so they stay warm all year round, even when snow is falling around the swimmers. The English word “geyser”, a spring that shoots hot water into the air, comes from Geysir, a famous hot spring in Iceland.\n\n"
                "For the people of Iceland, the forces that shape their island are both a danger and a gift. Scientists watch the volcanoes closely, measuring tiny earthquakes and the swelling of the ground, so that warnings can be given before an eruption. Life here means living with the land rather than against it.",
        "qs": [
            {"id": "1619d7346822", "t": "mcq", "d": "retrieve",
             "q": "According to the text, why does Iceland have so many volcanoes?",
             "opts": ["It sits where two plates are pulling apart", "It lies just south of the Arctic Circle",
                      "Its glaciers press down on the hot rock", "Its hot water is piped deep underground"],
             "no": {"Its glaciers press down on the hot rock": "Glaciers lie on some volcanoes, but the text says the volcanoes come from magma rising between the plates."},
             "why": "The second paragraph: as the two plates separate, magma rises to fill the gap. “This is why Iceland has so many volcanoes.”"},
            {"id": "5c43040ed5f5", "t": "text", "d": "vocab",
             "q": "Find and copy the word the text uses for hot molten rock under the ground.",
             "a": ["magma"],
             "why": "The second paragraph: “hot molten rock, called magma, rises to fill the gap.”"},
            {"id": "964f0feb8bab", "t": "mcq", "d": "retrieve",
             "q": "What is a jökulhlaup?",
             "opts": ["A sudden flood from an eruption under a glacier",
                      "A valley where the ground splits between plates",
                      "A cloud of volcanic ash that drifts over Europe",
                      "A hot spring that shoots water into the air"],
             "no": {"A hot spring that shoots water into the air": "That is a geyser, explained in the fifth paragraph."},
             "why": "The third paragraph explains that meltwater from an eruption under ice bursts out in a sudden flood, which Icelanders call a jökulhlaup."},
            {"id": "2f3a57d7c01e", "t": "mcq", "d": "retrieve",
             "q": "According to the text, why do Iceland’s outdoor swimming pools stay warm even when snow is falling?",
             "opts": ["They are filled with water heated underground by hot rock",
                      "They are heated by electricity from rivers fed by glaciers",
                      "They are built inside the craters of active volcanoes",
                      "They are only open in the warmest months of the year"],
             "no": {"They are heated by electricity from rivers fed by glaciers": "The rivers make electricity, but the text says the pools “are filled with this naturally hot water”.",
                    "They are only open in the warmest months of the year": "The text says the pools stay warm “all year round”, even in the snow."},
             "why": "The fifth paragraph: water seeping underground is heated by hot rock, and the pools “are filled with this naturally hot water too”.",
             "why2": "“This naturally hot water” points back to the rainwater and meltwater heated by hot rock at the start of the paragraph."},
            {"id": "57bb6446b797", "t": "tap", "d": "vocab",
             "q": "Tap the word that shows the smell of eggs is only slight.",
             "s": "The hot water comes out of the tap smelling [faintly] of eggs, because it contains a gas called hydrogen sulphide.",
             "why": "“Faintly” means only a little: the smell is there, but weak."},
            {"id": "a56cad94fedb", "t": "mcq", "d": "compare",
             "q": "The last paragraph calls the forces under Iceland “both a danger and a gift”. Which pair of details from the text shows both sides?",
             "opts": ["Sudden floods from eruptions; homes heated by hot water",
                      "Plates pulling apart; magma rising into the gap",
                      "Warm pools in the snow; electricity from rivers",
                      "Ash clouds over Europe; flights being cancelled"],
             "no": {"Warm pools in the snow; electricity from rivers": "Both of these are gifts: neither is a danger.",
                    "Ash clouds over Europe; flights being cancelled": "Both of these are part of the danger: neither is a gift."},
             "why": "A jökulhlaup is a danger; free heating from hot rock is a gift. The other pairs show only one side, or neither."},
            {"id": "cb85f98dc916", "t": "mcq", "d": "structure",
             "q": "Which best describes how the text is organised?",
             "opts": ["It explains the “fire”, then the “ice”, then their effects and how people live with them",
                      "It tells the story of one Icelandic family through a whole year",
                      "It describes Iceland’s volcanoes one by one, from largest to smallest",
                      "It compares Iceland with England, one paragraph at a time"],
             "no": {"It compares Iceland with England, one paragraph at a time": "England is mentioned only once, in the first sentence, to give the size."},
             "why": "Paragraph two begins “The fire comes from below”, paragraph three “The ice comes from above”; then come the 2010 ash cloud, the benefits, and a conclusion."},
        ],
    },
    {
        "key": "RD7.15",
        "year": 7,
        "strand": "Poems",
        "title": "Before the Shoppers Come",
        "nc": "Read poetry; explain how language, including figurative language, and structure create meaning and mood",
        "text": "At five o’clock the square is grey and still,\n"
                "the shutters down like eyelids on the shops;\n"
                "a pigeon struts across the empty stones,\n"
                "then stops, and listens, and once more it stops.\n"
                "The town is sleeping. Only we are here.\n\n"
                "Then Dad unbolts the van, and with a clank\n"
                "the metal poles come tumbling to the ground;\n"
                "we slot them into joints we know by heart\n"
                "and stretch the stripy canvas all around,\n"
                "and slowly, pole by pole, our stall stands up.\n\n"
                "Across the way, Miss Campbell hums a tune\n"
                "and builds her yams and peppers, carefully piled\n"
                "in tidy towers, golden, green and red;\n"
                "she says her mother hummed it in Kingston\n"
                "on market days, when she was still a child.\n\n"
                "Old Stan, the fishman, rubs his frozen hands\n"
                "and lays his silver mackerel out in rows\n"
                "on beds of crushed white ice, their round eyes wide,\n"
                "as if surprised the sea had let them go.\n"
                "He winks at me. He’s done this forty years.\n\n"
                "The flower stall is waking: buckets fill\n"
                "with tulips folded tight like sleepy fists,\n"
                "and daffodils that shout their yellow news\n"
                "to no one yet, and ferns, and dripping twists\n"
                "of green I cannot name, all cold and sweet.\n\n"
                "The sky begins to blush above the roofs.\n"
                "A bus yawns past. A window flickers bright.\n"
                "The first few shoppers wander in with bags,\n"
                "still blinking at the cold and the new light,\n"
                "and Dad calls out the prices of the day.\n\n"
                "And now the square is loud: “Two for a pound!”\n"
                "“Who’s next?” “Fresh strawberries! Come and see!”\n"
                "The coffee van is hissing out its steam,\n"
                "the coins are clinking, and a dog barks free\n"
                "of someone’s lead and runs off with a bun.\n\n"
                "I weigh the apples, count the change out twice,\n"
                "and learn the regulars by name and face:\n"
                "the man who buys one lemon every week,\n"
                "the student with her sketchbook and her case,\n"
                "the twins who always argue over plums.\n\n"
                "By nine the crowds are thick, and no one knows\n"
                "the square was ever grey, or hushed, or bare;\n"
                "they never saw the town before it woke.\n"
                "They only see the market. I was there.\n"
                "I watched it rise, like bread, from nothing much,\n"
                "and every Saturday I watch again.",
        "qs": [
            {"id": "987824556c18", "t": "mcq", "d": "language",
             "q": "“The shutters down like eyelids on the shops.” What does this simile suggest about the shops?",
             "opts": ["They seem to be asleep, with their eyes closed",
                      "They seem to be watching the narrator closely",
                      "They seem to be old, tired and falling apart",
                      "They seem to be crying because they are empty"],
             "no": {"They seem to be watching the narrator closely": "Eyelids that are down are closed, so the shops are not watching."},
             "why": "Closed shutters are like closed eyelids, and the verse ends “The town is sleeping”.",
             "why2": "Look at the last line of the verse: the whole town is asleep, and the shops have their 'eyes' shut."},
            {"id": "a3fb23fc59ce", "t": "mcq", "d": "infer",
             "q": "“We slot them into joints we know by heart.” What does this line suggest?",
             "opts": ["They have put the stall up many times before",
                      "They are learning to build the stall for the first time",
                      "They find the stall difficult and confusing to build",
                      "They have written instructions to follow on the van"],
             "why": "To know something by heart is to know it without thinking, which comes from doing it again and again."},
            {"id": "1110f215ba4a", "t": "text", "d": "retrieve",
             "q": "Find and copy the word that names the vegetables Miss Campbell piles up with her peppers.",
             "a": ["yams", "yam"],
             "why": "The third verse: she “builds her yams and peppers, carefully piled”."},
            {"id": "f9eb137075f7", "t": "mcq", "d": "infer",
             "q": "“He winks at me. He’s done this forty years.” What do these lines suggest about Old Stan?",
             "opts": ["He is relaxed and friendly after years of early starts",
                      "He is new to the market and nervous about the day",
                      "He is tired of the work and wants to stop soon",
                      "He is annoyed that the narrator is watching him"],
             "no": {"He is tired of the work and wants to stop soon": "Forty years is a long time, but a wink is playful and cheerful, not weary."},
             "why": "A wink is a friendly, joking gesture, and forty years of setting up means the cold, early start is nothing new to him."},
            {"id": "4132626ccab8", "t": "tap", "d": "language",
             "q": "Tap the word that makes the bus seem like a sleepy person.",
             "s": "A bus [yawns] past.",
             "why": "People yawn when they are tired; the bus seems as sleepy as the town still waking up."},
            {"id": "c6db211a2af3", "t": "mcq", "d": "structure",
             "q": "How does the mood change between the first verse and the seventh verse?",
             "opts": ["From quiet and still to noisy and busy",
                      "From busy and cheerful to calm and sad",
                      "From cold and gloomy to frightening and tense",
                      "From noisy and crowded to silent and empty"],
             "no": {"From noisy and crowded to silent and empty": "This is the wrong way round: the square starts empty and ends crowded."},
             "why": "Verse one is grey and still with “only we” there; verse seven is full of voices, steam, clinking coins and a barking dog."},
            {"id": "20e46775a4bb", "t": "mcq", "d": "summarise",
             "q": "What is the main idea of the last verse?",
             "opts": ["The narrator values having seen the market grow from nothing, which shoppers never see",
                      "The narrator wishes the shoppers would come earlier to help set up",
                      "The narrator is tired of getting up so early every Saturday",
                      "The narrator thinks the market was better when it was empty"],
             "no": {"The narrator is tired of getting up so early every Saturday": "“Every Saturday I watch again” sounds proud and willing, not tired."},
             "why": "“They only see the market. I was there.” The short sentence shows pride in a secret the crowds have missed."},
        ],
    },
    {
        "key": "RD7.16",
        "year": 7,
        "strand": "Letters and diaries",
        "title": "The bees next door",
        "nc": "Read diaries; infer the writer's feelings and how they change; explain the effect of language and comparison",
        "text": "Saturday 3 June\n"
                "Mr Pryce next door has asked whether I would like to help with his bees this summer. Mum said yes before I could open my mouth, because she says I spend far too long indoors. I said yes too, but only because it seemed rude to say no. I am not exactly a fan of things that sting.\n\n"
                "Sunday 4 June\n"
                "First visit to the hives. Mr Pryce lent me a white suit with a hood and a mesh veil, and gloves that came up to my elbows. He keeps three hives at the bottom of his orchard, wooden boxes painted pale green, and the air around them buzzed like a radio between stations.\n\n"
                "Before he opened the first hive, he puffed smoke at the entrance from a little tin can with bellows on the side. He says smoke calms the bees, so they are less likely to sting. Then he lifted out a frame, and it was covered in bees, thousands of them, crawling over one another without ever seeming to bump. I held my breath the whole time.\n\n"
                "Saturday 10 June\n"
                "I have learned some facts. Nearly all the bees in a hive are workers, and every worker is female. There is only one queen, and her job is to lay eggs: in summer she can lay more than a thousand a day. The males are called drones.\n\n"
                "Today I watched a worker come back to the hive and do a strange wiggling dance on the comb. Mr Pryce says it is called the waggle dance, and it tells the other bees which way to fly to find flowers.\n\n"
                "Saturday 17 June\n"
                "I got stung. A bee found its way up my sleeve, where the glove met the suit. It hurt for about ten minutes and then itched for two days. Mr Pryce said, “Welcome to beekeeping,” and showed me how to tuck my gloves in properly. He told me the bee would have died, because a honeybee’s sting stays stuck in the skin. I felt sorrier for her than for me. The strange thing is that I was less frightened afterwards. The worst had happened, and it was only a sting.\n\n"
                "Saturday 29 July\n"
                "Honey day! The frames at the top of the hives were heavy and sealed with a thin lid of pale wax. Mr Pryce explained that the bees make honey from nectar, the sweet juice in flowers, and fan it with their wings to dry it out before they seal it in. We sliced the wax off with a warm knife and spun the frames in a big metal drum until the honey ran out of a tap at the bottom, slow and golden.\n\n"
                "Thursday 31 August\n"
                "Last visit before school starts. I didn’t hold my breath once. I stood by the open hive and simply watched them coming and going, each one with a little load of yellow pollen on her back legs. On the way home I noticed that I call every bee “her” now, without even thinking about it. I have asked Mr Pryce if I can help again next year. He said the bees would be expecting me.",
        "qs": [
            {"id": "e45497cd2209", "t": "mcq", "d": "infer",
             "q": "Why did the writer first agree to help Mr Pryce?",
             "opts": ["She felt it would be impolite to refuse",
                      "She had always wanted to keep bees",
                      "She wanted to spend less time indoors",
                      "She hoped to be given some honey"],
             "no": {"She wanted to spend less time indoors": "That was Mum’s reason. The writer says she agreed “only because it seemed rude to say no”."},
             "why": "The first entry: she said yes “only because it seemed rude to say no”, and she is “not exactly a fan of things that sting”."},
            {"id": "721d612c512d", "t": "mcq", "d": "language",
             "q": "“The air around them buzzed like a radio between stations.” What does this simile suggest about the sound?",
             "opts": ["It was a steady, crackling hum that filled the air",
                      "It was a tune that the bees were playing together",
                      "It came and went as the bees flew far away",
                      "It was a message the bees were sending to Mr Pryce"],
             "no": {"It was a message the bees were sending to Mr Pryce": "A radio between stations picks up no programme at all: just a hiss, with no words or message."},
             "why": "A radio tuned between stations gives a constant fizzing hiss, like the hum of thousands of bees all around the hives."},
            {"id": "7403b34013bc", "t": "text", "d": "retrieve",
             "q": "Find and copy the word for the male bees in the hive.",
             "a": ["drones", "drone", "the drones"],
             "why": "The entry for 10 June: “The males are called drones.”"},
            {"id": "cfdcb634a77f", "t": "mcq", "d": "retrieve",
             "q": "According to the diary, what does the waggle dance do?",
             "opts": ["It shows other bees which way to fly to find flowers",
                      "It calms the bees before the hive is opened",
                      "It warns the hive that a beekeeper is coming",
                      "It tells the queen when it is time to lay eggs"],
             "no": {"It calms the bees before the hive is opened": "That is what the smoke does, in the entry for 4 June."},
             "why": "The entry for 10 June: the waggle dance “tells the other bees which way to fly to find flowers”."},
            {"id": "cda6456ea6ef", "t": "mcq", "d": "infer",
             "q": "Why was the writer less frightened of the bees after she was stung?",
             "opts": ["She had found that the thing she feared was bearable",
                      "Mr Pryce had given her a thicker suit to wear",
                      "She knew that bee could never sting anyone again",
                      "She was told the bees only sting once a summer"],
             "no": {"She knew that bee could never sting anyone again": "That one bee had died, but there were thousands of others: that is not why her fear went."},
             "why": "“The worst had happened, and it was only a sting”: the pain lasted ten minutes, so the fear had been bigger than the thing itself."},
            {"id": "09f0421a1950", "t": "tap", "d": "vocab",
             "q": "Tap the word that names the sweet juice from flowers that bees make into honey.",
             "s": "Mr Pryce explained that the bees make honey from [nectar], the sweet juice in flowers, and fan it with their wings to dry it out before they seal it in.",
             "why": "Nectar is the sugary liquid inside flowers; the bees dry it out to make honey."},
            {"id": "8f964d05aa84", "t": "mcq", "d": "compare",
             "q": "How has the writer changed between her first visit to the hives and her last?",
             "opts": ["She was too nervous to breathe; now she watches the bees calmly",
                      "She loved the bees at first; now she is tired of them",
                      "She was calm at first; now she is afraid after being stung",
                      "She wore a suit at first; now she works with no suit at all"],
             "no": {"She was calm at first; now she is afraid after being stung": "This is the wrong way round: she held her breath on 4 June, and after the sting she was less frightened."},
             "why": "On 4 June she “held my breath the whole time”; on 31 August she “didn’t hold my breath once” and “simply watched them”.",
             "why2": "Diaries often show change by echoing an early detail: holding her breath at the start, not holding it at the end, and asking to come back next year."},
        ],
    },
    {
        "key": "RD7.17",
        "year": 7,
        "strand": "Biography",
        "title": "Ada Lovelace",
        "nc": "Read a biography; retrieve and order information; recognise the writer's viewpoint and how evidence is weighed",
        "text": "In 1843, a young woman in London published a set of notes about a machine that did not exist. At the time, few people paid them much attention. More than a hundred years later, when the first computers were being built, her notes were read again. Her name was Ada Lovelace.\n\n"
                "Ada was born in London in 1815. Her father was the poet Lord Byron, famous across Europe for his poems and his stormy life. Her parents separated when she was only a few weeks old, and she never knew her father. Her mother, Annabella, was determined that Ada would not grow up wild and dreamy like him. Instead of poetry, she gave her daughter tutors in mathematics and science.\n\n"
                "Ada was often ill as a child, but her mind was restless. At about twelve, she decided she wanted to fly. She studied the wings of birds, compared materials such as paper, silk and feathers, and drew up plans for a flying machine. She never built it, but the project showed something that would stay with her all her life: she liked to take an idea and follow it as far as it would go.\n\n"
                "At seventeen, Ada met the mathematician Charles Babbage, who showed her part of a calculating machine he had built. She was fascinated. Babbage went on to design an even more ambitious machine, the Analytical Engine. It would be controlled by cards with holes punched in them, an idea borrowed from looms that wove patterns into cloth. The Analytical Engine was never finished, because it was too complicated and too expensive for the engineering of the time.\n\n"
                "In 1843, Ada translated an article about the engine written by an Italian engineer. She added her own notes, and they ended up about three times longer than the article itself. In one note she set out, step by step, how the engine could calculate a difficult series of numbers. Many people call this the first computer program.\n\n"
                "Her notes went further still. Babbage thought mainly of numbers. Ada saw that a machine which followed rules could work on anything that could be written as symbols: letters, or even musical notes. She imagined that such an engine might one day compose music. More than a hundred years before the first electronic computers, she had glimpsed what they might become.\n\n"
                "After her marriage, Ada became Countess of Lovelace, which is why we know her by that name. She died in 1852, aged only thirty-six.\n\n"
                "Historians still argue about how much of the work in the notes was hers and how much was Babbage’s. Yet the boldest idea, that a machine could do far more than arithmetic, is clearly her own. In 1980 a computer programming language was named Ada in her honour, and today she is remembered as one of the first people to understand what computers could really be.",
        "qs": [
            {"id": "5f8e0aea35ed", "t": "mcq", "d": "structure",
             "q": "Why does the writer begin with notes about “a machine that did not exist” rather than with Ada’s birth?",
             "opts": ["To make the reader curious before explaining who she was",
                      "To show that Ada’s notes were full of mistakes",
                      "To explain how the Analytical Engine was built",
                      "To prove that Ada was more famous than her father"],
             "why": "A puzzle (notes about a machine that did not exist, hardly noticed for a century) hooks the reader; her name is held back until the end of the paragraph.",
             "why2": "Biographies often open with a striking moment, then go back to the start of the life: here paragraph two goes back to 1815."},
            {"id": "81da0a5d7b2a", "t": "mcq", "d": "infer",
             "q": "Why did Ada’s mother give her tutors in mathematics and science?",
             "opts": ["She hoped to keep Ada from becoming like her father",
                      "She wanted Ada to help Charles Babbage with his machine",
                      "Ada was too ill as a child to go to school",
                      "Ada had asked to learn how to build a flying machine"],
             "no": {"She wanted Ada to help Charles Babbage with his machine": "Ada met Babbage at seventeen, long after her lessons began."},
             "why": "Annabella was determined Ada would not grow up “wild and dreamy” like Byron, so she chose maths and science “instead of poetry”."},
            {"id": "1ccda47bc295", "t": "mcq", "d": "retrieve",
             "q": "What did Ada do as part of her plan to fly?",
             "opts": ["She studied birds’ wings and compared materials",
                      "She built a flying machine from paper and silk",
                      "She asked Charles Babbage to design wings for her",
                      "She tested a small machine with feathers on it"],
             "no": {"She built a flying machine from paper and silk": "The text says she drew up plans but “never built it”."},
             "why": "The third paragraph: she studied the wings of birds, compared paper, silk and feathers, and drew up plans."},
            {"id": "11ae77510942", "t": "text", "d": "retrieve",
             "q": "Find and copy the name of the machine that Babbage designed but never finished.",
             "a": ["Analytical Engine", "the Analytical Engine"],
             "why": "The fourth paragraph: “Babbage went on to design an even more ambitious machine, the Analytical Engine.”"},
            {"id": "4ccde5cdb2fe", "t": "order", "d": "sequence",
             "q": "Put these events in Ada’s life in the order they happened.",
             "items": ["Her parents separated",
                       "She drew up plans for a flying machine",
                       "She met Charles Babbage",
                       "She published her notes on the Analytical Engine",
                       "She died, aged thirty-six"],
             "why": "Weeks old, about twelve, seventeen, 1843, then 1852."},
            {"id": "3168fc0ff24f", "t": "mcq", "d": "compare",
             "q": "According to the text, how did Ada’s view of the engine differ from Babbage’s?",
             "opts": ["He thought mainly of numbers; she saw it could work on any symbols",
                      "He wanted it to compose music; she wanted it to do sums",
                      "He thought it was too expensive; she thought it was cheap",
                      "He wanted it to weave cloth; she wanted it to do sums"],
             "no": {"He wanted it to compose music; she wanted it to do sums": "This is the wrong way round: music was Ada’s idea."},
             "why": "The sixth paragraph: “Babbage thought mainly of numbers. Ada saw that a machine which followed rules could work on anything that could be written as symbols.”"},
            {"id": "5ee7a3a689db", "t": "mcq", "d": "purpose",
             "q": "How does the writer deal with the question of how much of the work was Ada’s?",
             "opts": ["Admits historians disagree, but argues the boldest idea was hers",
                      "Says that Babbage did all the work and Ada took the credit",
                      "Ignores the question and praises Ada without any doubts",
                      "Says the notes were written entirely by Ada alone"],
             "no": {"Says the notes were written entirely by Ada alone": "The writer says historians still argue about this, so does not claim it."},
             "why": "The last paragraph: “Historians still argue…” then “Yet the boldest idea… is clearly her own.” The writer weighs both sides, then gives a view."},
        ],
    },
    {
        "key": "RD7.18",
        "year": 7,
        "strand": "News reports",
        "title": "Ospreys return to Hollin Mere",
        "nc": "Read news reports; distinguish fact from opinion; understand how a report is structured",
        "text": "A pair of ospreys has arrived at Hollin Mere nature reserve in Cumbria and moved into a nest platform built by local schoolchildren, the first time the birds have nested at the lake in living memory.\n\n"
                "The male was spotted on Tuesday morning by volunteer Jean Armstrong, 74, who has walked around the lake almost every day for thirty years. “I saw this great brown and white bird hovering over the water, and then it dropped like a stone and came up with a fish,” she said. “I had to sit down on the bench. I’ve waited half my life to see that here.” The female arrived two days later.\n\n"
                "The wooden platform stands on a tall pole above the reeds at the northern end of the lake. It was built last autumn by members of the wildlife club at Fellside Academy, with help from reserve staff. Twelve-year-old Ibrahim Sesay, who helped to carry the pole down to the shore, said: “Everyone said they probably wouldn’t come for years. When the ranger rang our school, the whole club went completely mad.”\n\n"
                "Ospreys are large birds of prey that live almost entirely on fish. They hunt by circling high above the water, then diving feet first to snatch a fish just below the surface. Every autumn they fly thousands of kilometres to spend the winter in West Africa, returning to Britain in spring.\n\n"
                "The birds were wiped out as nesting birds in England in the nineteenth century, when they were shot and their eggs were taken by collectors. A pair returned to nest in Scotland in the 1950s, and in 2001 ospreys nested naturally in England again, in the Lake District. Their numbers have been slowly rising ever since.\n\n"
                "Senior ranger Fiona Gallacher said the arrival was “the best news this reserve has had in decades”. She added: “Ospreys are fussy about where they nest. They need clean water, plenty of fish and somewhere high and quiet. The fact that they have chosen Hollin Mere tells us the lake is healthy.”\n\n"
                "Staff are asking visitors to stay on the marked paths and to keep well away from the northern shore, where a section of the path has been closed. Disturbing nesting ospreys is against the law. A camera fixed to a nearby tree is now sending live pictures of the nest to a screen in the visitor centre, so that people can watch the birds without disturbing them.\n\n"
                "If all goes well, the pair could raise chicks this summer. Ms Gallacher said: “We are keeping our fingers crossed. But even if they only stay a few weeks this year, they have found us, and ospreys often come back to the same nest year after year.”",
        "qs": [
            {"id": "d8b8e2453d65", "t": "mcq", "d": "structure",
             "q": "What is the job of the first paragraph of this report?",
             "opts": ["To sum up the main news in one sentence",
                      "To give the history of ospreys in England",
                      "To tell visitors which paths are closed",
                      "To describe how ospreys catch their fish"],
             "no": {"To give the history of ospreys in England": "The history comes much later, in the fifth paragraph."},
             "why": "News reports open with the key facts (who, what, where) in a single sentence; the details come after.",
             "why2": "A reader who stopped after the first paragraph would still know the main story: ospreys have nested on the children’s platform."},
            {"id": "5162a56ea5ed", "t": "mcq", "d": "infer",
             "q": "Jean Armstrong says, “I had to sit down on the bench.” What does this suggest?",
             "opts": ["She was overwhelmed by what she had seen",
                      "She was tired from walking around the lake",
                      "She was afraid the bird might attack her",
                      "She wanted to stay hidden from the bird"],
             "no": {"She was tired from walking around the lake": "She sat down straight after seeing the bird dive, and adds she had waited half her life for it."},
             "why": "She had “waited half her life” for this: the shock and joy were so great that she needed to sit down."},
            {"id": "24a223abb51e", "t": "tap", "d": "vocab",
             "q": "Tap the word that shows the osprey stayed in one place in the air before it dived.",
             "s": "“I saw this great brown and white bird [hovering] over the water, and then it dropped like a stone and came up with a fish,” she said.",
             "why": "To hover is to stay in one spot in the air, as the osprey does while it watches for a fish."},
            {"id": "debe35f47891", "t": "text", "d": "retrieve",
             "q": "Find and copy the name of the part of the world where ospreys spend the winter.",
             "a": ["West Africa"],
             "why": "The fourth paragraph: they fly thousands of kilometres “to spend the winter in West Africa”."},
            {"id": "95e227e7fd56", "t": "mcq", "d": "retrieve",
             "q": "Why did ospreys stop nesting in England in the nineteenth century?",
             "opts": ["They were shot, and collectors took their eggs",
                      "The lakes became too dirty for fish to live in",
                      "They began to spend the whole year in Africa",
                      "There were no tall poles or trees left to nest on"],
             "why": "The fifth paragraph: “they were shot and their eggs were taken by collectors”."},
            {"id": "104a0d3f157d", "t": "mcq", "d": "purpose",
             "q": "Which of these is an opinion rather than a fact?",
             "opts": ["The arrival is “the best news this reserve has had in decades”",
                      "Ospreys returned to nest in Scotland in the 1950s",
                      "A camera sends live pictures to the visitor centre",
                      "Disturbing nesting ospreys is against the law"],
             "why": "“The best news” is a judgement that people could disagree with; the others can be checked and proved."},
            {"id": "e935c591239d", "t": "mcq", "d": "retrieve",
             "q": "Why has a camera been fixed near the nest?",
             "opts": ["So visitors can see the birds while keeping their distance",
                      "So rangers can catch people who break the law",
                      "So the school can count how many fish are caught",
                      "So scientists can follow the birds to West Africa"],
             "no": {"So rangers can catch people who break the law": "The report says the camera sends pictures to the visitor centre “so that people can watch the birds without disturbing them”."},
             "why": "The seventh paragraph: the birds must not be disturbed, so the camera lets people watch them on a screen instead."},
        ],
    },
    {
        "key": "RD7.19",
        "year": 7,
        "strand": "Explanations",
        "title": "Why we have seasons",
        "nc": "Read explanations; follow a line of reasoning; understand how comparisons and examples help to explain",
        "text": "Ask people why summer is warmer than winter, and many will tell you that the Earth must be closer to the Sun in summer. It sounds sensible. It is also wrong. In fact, the Earth is at its closest to the Sun in early January, in the middle of the British winter. The real reason for the seasons is a tilt.\n\n"
                "The Earth spins on its axis, an imaginary line running through it from the North Pole to the South Pole. This axis is not straight up and down compared with the Earth’s path around the Sun. It leans over by about 23 degrees, and, as the Earth makes its year-long journey around the Sun, the axis keeps pointing in the same direction in space.\n\n"
                "This means that for part of the year the northern half of the Earth, the Northern Hemisphere, is tilted towards the Sun. Six months later, when the Earth has travelled to the other side of its orbit, the Northern Hemisphere is tilted away. The United Kingdom is in the Northern Hemisphere, so when our half leans towards the Sun, we have summer.\n\n"
                "Two things make a hemisphere warmer when it leans towards the Sun. The first is the angle of the sunlight. You can see the effect with a torch in a dark room. Shine it straight down at the floor and it makes a small, bright circle. Tilt it, and the same light spreads out over a larger, dimmer patch. In summer the Sun climbs high in the sky, and its light strikes the ground more directly, so each square metre receives more energy. In winter the Sun stays low, and its light is spread thinly, like the beam from the tilted torch.\n\n"
                "The second is the length of the day. In summer the Sun rises early and sets late, so the ground has more hours to warm up and fewer hours of darkness in which to cool down. In London, the longest day, in late June, has around sixteen and a half hours of daylight; the shortest, in late December, has only about eight.\n\n"
                "Because the two hemispheres lean in opposite directions, their seasons are opposite too. When it is summer in Britain, it is winter in Australia, and families in Sydney may be wrapped up in coats while people in Manchester are having picnics.\n\n"
                "Near the equator, the Sun is high in the sky all year round, and the length of the day hardly changes, so there is little difference between summer and winter. Near the poles, the difference is extreme. Around midsummer the Sun does not set at all for weeks or even months, and around midwinter it does not rise.\n\n"
                "So the seasons are not about distance at all. They are about the angle at which our planet meets the Sun.",
        "qs": [
            {"id": "641e1619036b", "t": "mcq", "d": "structure",
             "q": "Why does the writer begin with a mistaken idea about the seasons?",
             "opts": ["To grab attention by correcting a belief many readers hold",
                      "To show that the writer used to believe it as well",
                      "To prove that the Earth never changes its distance from the Sun",
                      "To explain why January is the coldest month in Britain"],
             "no": {"To prove that the Earth never changes its distance from the Sun": "The text says the Earth is closest in January, so its distance does change; it just does not cause the seasons."},
             "why": "Opening with a common mistake, then saying “It is also wrong”, makes the reader want to know the real reason.",
             "why2": "Writers of explanations often start from what readers already think, then overturn it: here the tilt replaces the distance idea."},
            {"id": "38f8a972e9fc", "t": "text", "d": "vocab",
             "q": "Find and copy the word that names the imaginary line from the North Pole to the South Pole.",
             "a": ["axis", "its axis"],
             "why": "The second paragraph: “The Earth spins on its axis, an imaginary line running through it from the North Pole to the South Pole.”"},
            {"id": "bbafc425b5aa", "t": "mcq", "d": "retrieve",
             "q": "According to the text, when is the Earth at its closest to the Sun?",
             "opts": ["In early January", "In late June", "In late December", "In midsummer"],
             "no": {"In late June": "Late June has London’s longest day, but the first paragraph says the Earth is closest in early January."},
             "why": "The first paragraph: “the Earth is at its closest to the Sun in early January, in the middle of the British winter”."},
            {"id": "7e43ca9fefd4", "t": "mcq", "d": "language",
             "q": "Why does the writer describe shining a torch in a dark room?",
             "opts": ["To give an everyday example of how angled light spreads out",
                      "To show that the Sun is much brighter than a torch",
                      "To explain why the days are shorter in winter",
                      "To suggest an experiment for measuring temperature"],
             "no": {"To explain why the days are shorter in winter": "Day length is the second reason, in the next paragraph; the torch explains the first, the angle of the light."},
             "why": "The straight beam makes a small bright circle; the tilted one a larger, dimmer patch, just like high summer Sun and low winter Sun."},
            {"id": "f31c03f7a70e", "t": "tap", "d": "vocab",
             "q": "Tap the word that shows the winter sunlight is not concentrated in one place.",
             "s": "In winter the Sun stays low, and its light is spread [thinly], like the beam from the tilted torch.",
             "why": "Light spread thinly covers a large area, so each part of the ground gets less of it."},
            {"id": "d99ce48c99bd", "t": "mcq", "d": "infer",
             "q": "Using the text, what season would Sydney have in late December?",
             "opts": ["Summer", "Winter", "Autumn", "Spring"],
             "no": {"Winter": "Late December is winter in Britain; the text says the two hemispheres have opposite seasons."},
             "why": "Late December is winter in Britain, and the seasons in Australia are the opposite of ours, so it is summer there.",
             "why2": "The text says “When it is summer in Britain, it is winter in Australia”: the reverse is also true."},
            {"id": "e25d7e4e177f", "t": "mcq", "d": "compare",
             "q": "How do the seasons near the equator compare with those near the poles?",
             "opts": ["The equator changes little; the poles change hugely",
                      "The equator has the longest summers; the poles the shortest",
                      "Both have the same seasons as the United Kingdom",
                      "The equator is always dark; the poles are always light"],
             "why": "The seventh paragraph: near the equator there is “little difference”; near the poles “the difference is extreme”."},
        ],
    },
    {
        "key": "RD7.20",
        "year": 7,
        "strand": "Persuasive writing",
        "title": "Why every pupil should learn to cook",
        "nc": "Read persuasive writing; identify the writer's viewpoint and the techniques used to persuade; tell fact from opinion",
        "text": "Last summer, my cousin went away to university. He was clever, organised and ready for anything, or so we thought. Three weeks later he rang my aunt in a panic. He had eaten toast for breakfast, toast for lunch and, on a good day, toast with beans for tea. He had no idea how to cook a single proper meal.\n\n"
                "He is not alone. Every year, thousands of young people leave home without knowing how to feed themselves. That is why I believe that every pupil in this school should learn to cook, properly and regularly, from Year 7 to Year 11.\n\n"
                "First, cooking is a skill for life. You might never use algebra at the supermarket, but you will need to eat every single day for the rest of your life. Knowing how to turn a few simple ingredients into a hot, healthy meal is not a luxury. It is as basic as being able to read a timetable or swim a length.\n\n"
                "Second, cooking is good for our health. When you make a meal yourself, you know exactly what goes into it: how much salt, how much sugar, how much fat. Ready meals and takeaways often contain far more of these than we realise. A pupil who can make a simple vegetable curry or a pan of soup has a real choice about what to eat.\n\n"
                "Third, cooking saves money. A bag of rice, a tin of tomatoes and a few onions cost very little, and they can make several meals. Buying the same number of meals ready-made costs far more. Surely a school that teaches us about budgets in maths should also teach us how to stick to one in the kitchen?\n\n"
                "Some people will say that there is no time for cooking in a crowded timetable, and that it is a job for parents, not schools. I understand this. Teachers are already very busy, and exams matter. But not every family has the time to teach cooking at home, and a lesson every fortnight would hardly bring the school to a standstill. Besides, cooking uses maths when we weigh and measure, science when we see what heat does to food, and teamwork when we share a kitchen. It does not take time away from learning; it is learning.\n\n"
                "Finally, cooking brings people together. Some of my happiest memories are of making flatbreads with my grandmother, flour everywhere, laughing as we tried to roll them into circles. A meal you have made yourself and shared with others is worth ten eaten alone in front of a screen.\n\n"
                "So I am asking the head teacher and the governors to give every year group regular cooking lessons. Give us the skills, and we will do the rest. My cousin has learned now, by the way. He makes a very good omelette. But he wishes he had learned at school.\n\n"
                "Sana Iqbal, Year 9",
        "qs": [
            {"id": "8e1015d7e9d8", "t": "mcq", "d": "structure",
             "q": "Why does Sana begin with the story about her cousin?",
             "opts": ["To give a real example that makes the problem feel personal",
                      "To show that her cousin is not as clever as people thought",
                      "To explain what students eat at university",
                      "To prove that toast is an unhealthy food"],
             "no": {"To show that her cousin is not as clever as people thought": "She says he was clever and organised: the point is that even he had never learned to cook."},
             "why": "An anecdote draws the reader in and shows the problem through one real person before the argument begins.",
             "why2": "Persuasive writers often open with a short true story: the reader cares about the cousin, then hears “He is not alone”."},
            {"id": "07f1f3cbb9cc", "t": "mcq", "d": "language",
             "q": "“Surely a school that teaches us about budgets in maths should also teach us how to stick to one in the kitchen?” What technique is this?",
             "opts": ["A rhetorical question that expects the reader to agree",
                      "A simile comparing a school to a kitchen",
                      "A fact proved by figures from a survey",
                      "A counter-argument that Sana disagrees with"],
             "no": {"A counter-argument that Sana disagrees with": "This is Sana’s own point; the counter-argument comes in the next paragraph."},
             "why": "It is asked not to be answered but to make the answer seem obvious; “Surely” pushes the reader to say yes."},
            {"id": "d0ad83809545", "t": "tap", "d": "language",
             "q": "Tap the word Sana uses to show she sees cooking as something everyone needs, not an extra treat.",
             "s": "It is as [basic] as being able to read a timetable or swim a length.",
             "why": "Something basic is a simple essential that everyone needs, which is the opposite of the luxury in the sentence before."},
            {"id": "efe4c2d10c7a", "t": "mcq", "d": "structure",
             "q": "What does Sana do in the paragraph beginning “Some people will say”?",
             "opts": ["Gives the other side’s view, then argues against it",
                      "Admits she was wrong and changes her mind",
                      "Lists more reasons why cooking saves money",
                      "Tells a second story about her family"],
             "why": "She sets out the objection (no time, a job for parents), agrees it has some sense, then answers it with “But…” and “Besides…”."},
            {"id": "ee9a8114cd02", "t": "mcq", "d": "infer",
             "q": "What does Sana mean by “It does not take time away from learning; it is learning”?",
             "opts": ["Cooking lessons teach maths, science and teamwork too",
                      "Pupils could learn to cook during their maths lessons",
                      "Cooking is more important than every other subject",
                      "Pupils should cook at home instead of doing homework"],
             "no": {"Pupils could learn to cook during their maths lessons": "She asks for cooking lessons of their own; her point is that they use maths, not that they replace it."},
             "why": "Just before, she lists the maths in weighing, the science in heating food and the teamwork in sharing a kitchen: cooking is a lesson in itself."},
            {"id": "bfae4f015070", "t": "mcq", "d": "purpose",
             "q": "Which of these is a fact rather than an opinion?",
             "opts": ["Cooking uses weighing and measuring",
                      "Cooking is the best way to learn teamwork",
                      "A shared meal is worth ten eaten alone",
                      "Every pupil should learn to cook"],
             "no": {"A shared meal is worth ten eaten alone": "This is Sana’s feeling: “worth ten” cannot be measured or proved."},
             "why": "You can check that recipes involve weighing and measuring; the others are judgements people could disagree with."},
            {"id": "92886608784a", "t": "mcq", "d": "purpose",
             "q": "Who is Sana mainly trying to persuade, and what does she want them to do?",
             "opts": ["The head teacher and governors, to give every year group cooking lessons",
                      "Her cousin, to learn to cook before he goes back to university",
                      "Parents, to teach their children to cook at home",
                      "Other pupils, to make flatbreads with their grandparents"],
             "no": {"Parents, to teach their children to cook at home": "She says not every family has time for this: she wants schools to do it."},
             "why": "The last paragraph: “I am asking the head teacher and the governors to give every year group regular cooking lessons.”"},
        ],
    },
    {
        "key": "RD7.21",
        "year": 7,
        "strand": "Play scripts",
        "title": "The greenhouse",
        "nc": "Read a play script; infer characters' feelings and motives from dialogue and stage directions",
        "text": "(The shared back garden behind a block of flats in Glasgow. Late afternoon. At one side stands a small greenhouse; one pane of glass is smashed. A football lies among the tomato plants inside. CALLUM, 11, stands frozen. His sister ISLA, 13, runs out from the back door.)\n"
                "ISLA: What was that noise? (She sees the greenhouse.) Oh, Callum. Tell me that’s not your ball.\n"
                "CALLUM: It bounced off the wall. It wasn’t even a hard kick.\n"
                "ISLA: That’s Mr Duncan’s greenhouse. He’s been growing those tomatoes since March.\n"
                "CALLUM: (looking up at the windows) Nobody saw. If I get the ball out quickly, he’ll think it was the wind. Or a bird.\n"
                "ISLA: A bird. A bird that plays football.\n"
                "CALLUM: Isla, please. He’ll tell Mum. He’ll want money for the glass, and I’ve only got four pounds.\n"
                "ISLA: (quietly) And what happens when he finds the ball in his tomatoes and your name written on it in marker pen?\n"
                "(CALLUM looks at the ball. His shoulders drop.)\n"
                "CALLUM: I forgot about that.\n"
                "ISLA: Come on. I’ll come with you. It’ll be worse if he has to come and find us.\n"
                "(They cross to the ground-floor door and knock. A long pause. MR DUNCAN, in his seventies, opens it, holding a mug of tea.)\n"
                "MR DUNCAN: Afternoon, you two.\n"
                "CALLUM: (all in one breath) Mr Duncan, I’m really sorry, I kicked my ball and it went through your greenhouse and one of the panes is broken and I’ll pay for it, I’ve got four pounds, and I can get more.\n"
                "(MR DUNCAN looks at him for a long moment. Then he takes a slow sip of tea.)\n"
                "MR DUNCAN: I know. I was at the kitchen window.\n"
                "CALLUM: (horrified) You saw?\n"
                "MR DUNCAN: I saw. And then I put the kettle on and waited to see whether anybody would knock on my door. (He looks at ISLA.) I had a feeling one of you might.\n"
                "ISLA: It was Callum’s idea to come, really.\n"
                "(CALLUM stares at her. She gives him a tiny shake of the head.)\n"
                "MR DUNCAN: Well. Keep your four pounds, son. A pane of glass costs more than that. But I’ve a bag of compost that needs carrying, and the tomatoes will want watering every evening while I’m at my daughter’s next week. Would that seem fair?\n"
                "CALLUM: Every evening?\n"
                "ISLA: (nudging him) He means yes.\n"
                "CALLUM: Yes. Yes, that’s fair. Thank you.\n"
                "MR DUNCAN: (turning to go in, then stopping) When I was about your age, I put a cricket ball through the window of our school hall.\n"
                "CALLUM: What did you do?\n"
                "MR DUNCAN: I ran. (He smiles.) It took me two days to own up, and they were the longest two days of my life. You did it in two minutes. Get your ball, Callum.\n"
                "(He goes inside. CALLUM and ISLA look at each other. Lights fade.)",
        "qs": [
            {"id": "077f00b29996", "t": "mcq", "d": "infer",
             "q": "Callum says, “It bounced off the wall. It wasn’t even a hard kick.” Why does he say this?",
             "opts": ["He is trying to make the accident seem less his fault",
                      "He is proud of how far he can kick a football",
                      "He wants Isla to know the wall is damaged too",
                      "He is explaining to Mr Duncan exactly what happened"],
             "no": {"He is explaining to Mr Duncan exactly what happened": "Mr Duncan is not there yet: Callum is talking to Isla."},
             "why": "Both remarks are excuses: the wall and the soft kick are to blame, he suggests, not him."},
            {"id": "1cb512a01e32", "t": "mcq", "d": "language",
             "q": "Isla replies, “A bird. A bird that plays football.” What does this show?",
             "opts": ["She thinks his plan to blame a bird is ridiculous",
                      "She has seen a bird near the greenhouse",
                      "She agrees that the wind could have broken the glass",
                      "She is joking to make Mr Duncan laugh"],
             "no": {"She has seen a bird near the greenhouse": "She repeats Callum’s word to mock it, not to report a real bird."},
             "why": "She repeats his idea and adds an absurd detail: sarcasm that shows nobody would believe it."},
            {"id": "2b75bf3362d0", "t": "mcq", "d": "retrieve",
             "q": "What does Isla point out that would give Callum away?",
             "opts": ["His name is written on the ball", "Mr Duncan was watching from the window",
                      "The ball is the only one in the garden", "Their mum heard the glass break"],
             "no": {"Mr Duncan was watching from the window": "That is true, but nobody knows it until Mr Duncan says so later."},
             "why": "Isla asks what will happen when Mr Duncan finds the ball “and your name written on it in marker pen”."},
            {"id": "ed2e8e43d771", "t": "tap", "d": "infer",
             "q": "Tap the verb in the stage direction that shows Callum has given up his plan to hide what he did.",
             "s": "His shoulders [drop].",
             "why": "Dropped shoulders show someone giving in: he realises his plan cannot work."},
            {"id": "a60e9f98a739", "t": "mcq", "d": "infer",
             "q": "Why does Isla say, “It was Callum’s idea to come, really”?",
             "opts": ["To help Mr Duncan think well of her brother",
                      "To make sure Callum gets all the blame",
                      "To correct a mistake Mr Duncan has made",
                      "To show that she did not want to come at all"],
             "no": {"To correct a mistake Mr Duncan has made": "It was really Isla’s idea; her small shake of the head tells Callum to go along with it."},
             "why": "It was her idea, so she is giving him the credit; the tiny shake of the head tells Callum not to argue."},
            {"id": "33d03bf8fa2b", "t": "text", "d": "retrieve",
             "q": "Find and copy the word that names what Callum must water every evening.",
             "a": ["tomatoes", "the tomatoes", "tomato", "tomato plants", "the tomato plants"],
             "why": "Mr Duncan says “the tomatoes will want watering every evening while I’m at my daughter’s next week”."},
            {"id": "2b9c54155931", "t": "mcq", "d": "compare",
             "q": "How was Mr Duncan’s behaviour as a boy different from Callum’s today?",
             "opts": ["He ran away and took days to own up; Callum owned up in minutes",
                      "He paid for the window; Callum was told to keep his money",
                      "He blamed a bird; Callum blamed the wind",
                      "He owned up at once; Callum tried to run away"],
             "no": {"He owned up at once; Callum tried to run away": "This is the wrong way round: Mr Duncan says “I ran.”"},
             "why": "“I ran… It took me two days to own up… You did it in two minutes.” He contrasts the two to praise Callum."},
        ],
    },
    {
        "key": "RD7.22",
        "year": 7,
        "strand": "Stories",
        "title": "The golden crack",
        "nc": "Make inferences and refer to evidence in the text; explain how a writer uses an object to carry a story's meaning",
        "text": "Haruto had been at his grandmother’s house in Kyoto for a week before he told her about the competition.\n\n"
                "He had not meant to tell her at all. He had come to stay for the summer holidays, as he did every year, and he had planned to spend it reading comics on the cool wooden floor and not thinking about calligraphy ever again. But on the seventh evening, as they were washing up together, she asked whether he had brought his brushes.\n\n"
                "“I’ve stopped,” he said. “I left the club.”\n\n"
                "His grandmother went on drying a plate. She did not ask why. She simply waited, and the silence did the asking for her.\n\n"
                "So he told her. He had practised for the school competition for three months, writing the same four characters hundreds of times. On the day, with the judges watching, his hand had shaken on the very last stroke, and a fat drop of ink had fallen onto the paper. One blot, the size of a fingernail, and the whole piece was ruined. Everyone had been kind about it, which had somehow made it worse.\n\n"
                "As he finished the story, the bowl he was holding slid out of his wet hands. It hit the stone floor with a sharp crack and broke cleanly into three pieces.\n\n"
                "Haruto stared at it. It was his grandmother’s favourite bowl, pale grey with a soft blue glaze, and it had belonged to her mother. “I’m sorry,” he said. His voice came out very small. “I’m so sorry, Obaachan.”\n\n"
                "To his surprise, she knelt down and gathered the pieces carefully into a cloth, as if they were something precious rather than something broken. “Don’t throw anything away,” she said. “Not even the tiny bits.”\n\n"
                "Over the next three weeks, he watched her mend it. She joined the pieces with a special lacquer made from the sap of a tree, a little at a time, and left each layer to harden for days in a damp cupboard. She was never in a hurry. At the very end, she dusted the last layer with fine gold powder.\n\n"
                "When she showed him the finished bowl, Haruto caught his breath. The cracks had not been hidden. They had been turned into bright golden rivers running across the grey glaze, and the bowl was somehow more beautiful than before.\n\n"
                "“This is called kintsugi,” she said. “Golden joinery. We do not pretend the bowl was never broken. The break is part of its story now.” She turned it gently in her hands. “And a story with a mistake in it is often more interesting than one without.”\n\n"
                "Haruto said nothing for a long time.\n\n"
                "On his last morning in Kyoto, before the train back to Osaka, his grandmother found him at the low table by the window. He had borrowed her old brush and was writing the same four characters, slowly and carefully, again and again.",
        "qs": [
            {"id": "6c02d0756e4f", "t": "mcq", "d": "retrieve",
             "q": "At the start, what had Haruto planned to do during the summer?",
             "opts": ["Relax and forget about calligraphy completely",
                      "Practise calligraphy for the next competition",
                      "Learn how to mend pottery with his grandmother",
                      "Spend his days exploring the streets of Kyoto"],
             "no": {"Practise calligraphy for the next competition": "He planned “not thinking about calligraphy ever again”, and had left the club."},
             "why": "The second paragraph: comics on the cool floor and “not thinking about calligraphy ever again”."},
            {"id": "3d6a289dcd93", "t": "mcq", "d": "language",
             "q": "“She simply waited, and the silence did the asking for her.” What does this suggest?",
             "opts": ["Her quiet patience made Haruto want to explain",
                      "She was too busy drying plates to talk to him",
                      "She was angry and refused to speak to Haruto",
                      "She had not heard what Haruto said to her"],
             "no": {"She was angry and refused to speak to Haruto": "Nothing suggests anger: she is waiting kindly, and he goes on to tell her everything."},
             "why": "The silence is personified as asking a question: by saying nothing she lets Haruto choose to tell her, and he does."},
            {"id": "d024d684348c", "t": "mcq", "d": "retrieve",
             "q": "What went wrong for Haruto in the competition?",
             "opts": ["His hand shook and a drop of ink fell on the paper",
                      "He forgot one of the four characters he had practised",
                      "The judges said his writing was far too small",
                      "He ran out of time before the very last stroke"],
             "why": "The fifth paragraph: “his hand had shaken on the very last stroke, and a fat drop of ink had fallen onto the paper”."},
            {"id": "26ed02dc12d1", "t": "tap", "d": "infer",
             "q": "Tap the word that shows Haruto felt guilty and upset when he apologised.",
             "s": "His voice came out very [small].",
             "why": "A small voice is quiet and weak: he is ashamed and frightened about breaking the precious bowl."},
            {"id": "0dc63bae26ee", "t": "mcq", "d": "compare",
             "q": "How does the grandmother’s reaction to the broken bowl differ from Haruto’s reaction to his blot of ink?",
             "opts": ["He saw the mistake as ruining everything; she treats the break as worth keeping",
                      "He laughed about the mistake; she is very upset by the break",
                      "He tried to hide the mistake; she wants to throw the pieces away",
                      "He fixed the mistake quickly; she takes weeks to decide what to do"],
             "no": {"He tried to hide the mistake; she wants to throw the pieces away": "She says “Don’t throw anything away”: she keeps every piece."},
             "why": "For Haruto “the whole piece was ruined” by one blot; she gathers the pieces “as if they were something precious”."},
            {"id": "b41f582365a8", "t": "text", "d": "retrieve",
             "q": "Find and copy the word that names the Japanese art of mending with gold.",
             "a": ["kintsugi"],
             "why": "The grandmother says, “This is called kintsugi. Golden joinery.”"},
            {"id": "b1042f15f8d2", "t": "mcq", "d": "structure",
             "q": "What does the last paragraph show, and how does it link back to earlier in the story?",
             "opts": ["He has started writing the same four characters again, so he has accepted his mistake",
                      "He is copying his grandmother’s writing, so he wants to join a new club",
                      "He is practising to please his grandmother, so she will forgive him",
                      "He is writing a letter about the bowl, so he still feels guilty"],
             "no": {"He is writing a letter about the bowl, so he still feels guilty": "He is writing “the same four characters” from the competition, not a letter."},
             "why": "The four characters are the ones from the competition he had given up: the bowl has taught him a mistake does not ruin everything.",
             "why2": "Look for what returns from earlier: “the same four characters”, written “again and again”, just as he once practised them."},
        ],
    },
    {
        "key": "RD7.23",
        "year": 7,
        "strand": "Information",
        "title": "Antarctica: the continent of extremes",
        "nc": "Read information texts; retrieve and record information; explain how a writer organises and presents facts",
        "text": "At the bottom of the world lies a continent bigger than Europe where nobody has ever lived permanently. Antarctica is the coldest, windiest and driest continent on Earth, and almost all of it, about ninety-eight per cent, is buried under ice.\n\n"
                "That ice is not a thin crust. In places the Antarctic ice sheet is more than four kilometres thick, so deep that it hides whole mountain ranges. It holds most of the fresh water on the planet. If it all melted, which would take thousands of years, sea levels around the world would rise by many metres.\n\n"
                "The cold is hard to imagine. The lowest natural temperature ever measured on Earth, minus 89.2 degrees Celsius, was recorded at a Russian research station called Vostok in 1983. At that temperature, a cup of hot water thrown into the air would freeze into a cloud of ice crystals before it hit the ground. Even in summer, much of the inland ice stays far below freezing.\n\n"
                "It may seem strange to call a place covered in ice a desert, but that is exactly what Antarctica is. A desert is defined not by heat or sand but by how little rain or snow falls there, and the high centre of Antarctica gets so little snow each year that it is one of the driest places on Earth. The ice has built up because almost none of the snow that does fall ever melts.\n\n"
                "The seasons are extreme too. Near the South Pole, the Sun stays above the horizon for months in summer, and in winter there are months of darkness. Few living things can survive on the land itself, but the seas around the coast are rich in life, from tiny shrimp-like krill to seals and whales. Emperor penguins survive the winter storms by huddling together in their thousands, taking turns to stand on the freezing outside edge of the group.\n\n"
                "Today the only people in Antarctica are scientists, support staff and visitors. An international agreement signed in 1959 set the continent aside for peaceful purposes and scientific research. A few thousand people work at research stations in summer, and far fewer stay through the long, dark winter.\n\n"
                "Their work matters to the whole planet. By drilling deep into the ice and pulling out long cylinders called ice cores, scientists can study tiny bubbles of air that were trapped when the snow fell, hundreds of thousands of years ago. These bubbles show what the Earth’s air and climate were like in the distant past. In 1985, scientists from the British Antarctic Survey reported that the ozone layer high above Antarctica was becoming thinner each spring. Their discovery led countries around the world to ban many of the chemicals that were damaging it.\n\n"
                "Antarctica may be the emptiest place on Earth, but it is far from unimportant. Its ice is a frozen record of our planet’s history, and the scientists who study it are helping us understand our future.",
        "qs": [
            {"id": "bc94c13e14a9", "t": "mcq", "d": "retrieve",
             "q": "According to the text, how much of Antarctica is covered by ice?",
             "opts": ["About ninety-eight per cent", "About half", "About four kilometres", "Most of the coast but not the centre"],
             "no": {"About four kilometres": "Four kilometres is how thick the ice is in places, not how much of the land it covers."},
             "why": "The first paragraph: “almost all of it, about ninety-eight per cent, is buried under ice”."},
            {"id": "48b1f2011a17", "t": "mcq", "d": "language",
             "q": "Why does the writer describe a cup of hot water freezing in the air?",
             "opts": ["To help the reader picture how extreme the cold is",
                      "To give instructions for an experiment to try at home",
                      "To explain why the research station is called Vostok",
                      "To show that scientists drink hot drinks to stay warm"],
             "why": "A number like minus 89.2 degrees is hard to feel; an image of boiling-hot water turning to ice crystals makes it vivid.",
             "why2": "The paragraph opens “The cold is hard to imagine”: the example is there to make it easier to imagine."},
            {"id": "7ccedeb30ac7", "t": "mcq", "d": "vocab",
             "q": "According to the text, what makes a place a desert?",
             "opts": ["How little rain or snow falls there",
                      "How hot it gets during the day",
                      "How much sand covers the ground",
                      "How few people choose to live there"],
             "no": {"How much sand covers the ground": "The text says a desert is defined “not by heat or sand”."},
             "why": "The fourth paragraph: a desert is defined “by how little rain or snow falls there”."},
            {"id": "2e78b34946bf", "t": "mcq", "d": "infer",
             "q": "Why do emperor penguins take turns on the outside edge of the group?",
             "opts": ["The outside is coldest, so sharing it means no penguin freezes",
                      "The outside is safest from seals and whales in the sea",
                      "The strongest penguins must always lead the way to the sea",
                      "The penguins on the outside are looking for krill to eat"],
             "no": {"The outside is safest from seals and whales in the sea": "The text links the huddle to surviving winter storms, not to escaping animals."},
             "why": "The text calls the outside edge “freezing”; taking turns means each penguin gets time in the warmer middle."},
            {"id": "816eb755f754", "t": "text", "d": "retrieve",
             "q": "Find and copy the two words that name the long cylinders of ice that scientists drill out.",
             "a": ["ice cores", "ice core", "the ice cores"],
             "why": "The seventh paragraph: “long cylinders called ice cores”."},
            {"id": "1f452a93e72b", "t": "tap", "d": "retrieve",
             "q": "Tap the word that tells you which layer high above Antarctica was becoming thinner.",
             "s": "In 1985, scientists from the British Antarctic Survey reported that the [ozone] layer high above Antarctica was becoming thinner each spring.",
             "why": "The scientists found the ozone layer was thinning each spring."},
            {"id": "89e38e7cdadb", "t": "mcq", "d": "structure",
             "q": "How does the last paragraph link to the first?",
             "opts": ["It returns to the idea of an empty place, then shows why it still matters",
                      "It repeats the list of the coldest, windiest and driest places",
                      "It gives new figures about how thick the ice sheet is",
                      "It tells the reader how to visit Antarctica safely"],
             "no": {"It repeats the list of the coldest, windiest and driest places": "That list is in the first paragraph only; the ending moves on to why Antarctica matters."},
             "why": "The first paragraph says nobody lives there; the last calls it “the emptiest place on Earth, but… far from unimportant”."},
        ],
    },
    {
        "key": "RD7.24",
        "year": 7,
        "strand": "Stories",
        "title": "Learning to row",
        "nc": "Make inferences and refer to evidence in the text; compare characters within a text; explain how structure shows change",
        "text": "Everyone in the family agreed that Chioma was good at things. She had won the county hurdles at fourteen, played the violin in the youth orchestra, and once learned to juggle in a single afternoon, just to prove she could. Her little sister Adaeze had watched all this for twelve years, and had decided, quite calmly, that she was not good at things.\n\n"
                "So nobody was more surprised than Adaeze when she signed up for the junior rowing course at the club on the River Trent. She was not even sure why she had done it. Perhaps it was because Chioma had never tried rowing, and so for once there would be nothing to be compared with.\n\n"
                "The first session was a disaster. The boat was long and narrow, hardly wider than her hips, and it rocked at the slightest movement. The coach, a cheerful woman called Kath with a voice that carried right across the water, showed her how to hold the oars, how to slide the seat, how to keep her hands level. Adaeze listened to every word. Then she pushed off from the landing stage, leaned a fraction too far to the left, and tipped slowly and gracefully into the river.\n\n"
                "The water was shockingly cold. Her life jacket brought her straight back up, spluttering, and Kath was beside her in the safety launch within seconds. “Everyone goes in once,” Kath said, hauling her out. “Some people go in ten times. It means you’re learning.”\n\n"
                "Adaeze did not go in ten times. She went in four. She went to every session anyway, every Tuesday evening and every Saturday morning, through the whole of the autumn term. Slowly, the boat stopped feeling like a wild animal trying to throw her off. She learned to feel the balance through her seat, to let the oars rest flat on the water when she wobbled, to breathe out on each stroke. Her hands blistered, then hardened. Chioma asked once how it was going, and Adaeze said, “Fine,” and changed the subject.\n\n"
                "One cold Saturday in December, she arrived early. Mist lay on the river like a sheet of grey wool, and the only sound was a pair of swans gliding past the boathouse. Kath looked at the water, then at Adaeze. “Go on,” she said. “Take it to the bridge and back.”\n\n"
                "Adaeze slid the boat out. The first stroke was clumsy, the second better. By the tenth, something clicked. The blades went in and came out cleanly, the seat slid smoothly beneath her, and the boat ran forward on its own between strokes, as though the river were helping. She reached the bridge, turned, and rowed back without a single wobble.\n\n"
                "When she climbed out onto the landing stage, someone was clapping. It was Chioma, wrapped in a big coat, holding a towel and Adaeze’s woolly hat.\n\n"
                "“Mum told me you’d be here,” she said, handing them over. She looked out at the narrow boat rocking gently on the water. “I don’t think I could do that,” she said. “Not even close.”\n\n"
                "Adaeze pulled the hat down over her ears with stiff fingers and, for the first time she could remember, did not say anything to make herself smaller.",
        "qs": [
            {"id": "f29ce6464e91", "t": "mcq", "d": "infer",
             "q": "Why might Adaeze have chosen rowing?",
             "opts": ["Chioma had never rowed, so she would not be compared with her",
                      "Chioma had told her that rowing was easy to learn",
                      "Her family wanted her to join the same club as Chioma",
                      "She had always been good at sports on the water"],
             "no": {"She had always been good at sports on the water": "She had decided she “was not good at things”, and the first session is a disaster."},
             "why": "The second paragraph: “Perhaps it was because Chioma had never tried rowing, and so for once there would be nothing to be compared with.”"},
            {"id": "d9122f58e8f9", "t": "mcq", "d": "language",
             "q": "Adaeze “tipped slowly and gracefully into the river”. What is the effect of “slowly and gracefully”?",
             "opts": ["It makes the fall gently funny, as if it happened in slow motion",
                      "It shows that Adaeze fell in on purpose to cool down",
                      "It suggests that she was a skilled and graceful rower",
                      "It shows the river was calm and very shallow there"],
             "no": {"It suggests that she was a skilled and graceful rower": "It is her very first session and she has just leaned “a fraction too far”: the grace is in the fall, not the rowing."},
             "why": "Falling in is not usually graceful: the unexpected words make the moment comic, like a slow-motion replay.",
             "why2": "Writers sometimes describe a mishap in elegant words for humour: we can picture her toppling over almost politely."},
            {"id": "d2727bb200a9", "t": "order", "d": "sequence",
             "q": "Put these in the order they happen in the story.",
             "items": ["Adaeze signs up for the rowing course",
                       "She falls in at her first session",
                       "She goes to every session through the autumn term",
                       "She rows to the bridge and back without a wobble",
                       "Chioma hands her a towel and her hat"],
             "why": "The story follows Adaeze from signing up, through the autumn of practice, to the misty December morning."},
            {"id": "46f0a0da423e", "t": "text", "d": "retrieve",
             "q": "Find and copy the number of times Adaeze fell into the river altogether.",
             "a": ["four", "4"],
             "why": "The fifth paragraph: “Adaeze did not go in ten times. She went in four.”"},
            {"id": "b52d7078bce4", "t": "tap", "d": "language",
             "q": "Tap the word in this sentence that shows how the mist looked soft and thick on the river.",
             "s": "Mist lay on the river like a sheet of grey [wool], and the only sound was a pair of swans gliding past the boathouse.",
             "why": "Wool is soft and thick: the simile shows the mist lying heavy and quiet over the water."},
            {"id": "8544cbf73d75", "t": "mcq", "d": "compare",
             "q": "What has changed between the two sisters by the end of the story?",
             "opts": ["Chioma now admires something Adaeze can do that she cannot",
                      "Adaeze now realises that Chioma is not good at anything",
                      "Chioma is now jealous and wants to take up rowing herself",
                      "Adaeze now wants to give up rowing and play the violin"],
             "no": {"Chioma is now jealous and wants to take up rowing herself": "She claps and brings a towel and hat: she is proud, not jealous, and says she could not do it."},
             "why": "At the start Adaeze watched Chioma do everything; at the end Chioma watches Adaeze and says, “I don’t think I could do that.”"},
            {"id": "6b1904763957", "t": "mcq", "d": "summarise",
             "q": "Which sentence best sums up the story?",
             "opts": ["Sticking at rowing helps Adaeze stop seeing herself as less than Chioma",
                      "Rowing is a dangerous sport that beginners should not try alone",
                      "Chioma turns out to be better than Adaeze at every sport she tries",
                      "A patient coach teaches a nervous girl to swim in a cold river"],
             "no": {"A patient coach teaches a nervous girl to swim in a cold river": "Adaeze learns to row, not swim, and the story is more about how she sees herself than about Kath."},
             "why": "It opens with Adaeze deciding she “was not good at things” and ends with her, for once, not making “herself smaller”: the rowing changes how she sees herself.",
             "why2": "A good summary covers the whole story: the comparison with Chioma at the start, the months of practice, and the proud ending."},
        ],
    },
]
