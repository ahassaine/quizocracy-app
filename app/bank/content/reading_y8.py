"""Reading comprehension, Year 8 (KS3).

Twelve original passages, written by hand for this bank (none copied or paraphrased from a published text),
each 350-550 words with seven questions. KS3 reading at Year 8 depth: implicit meaning and inference from
evidence, the writer's methods (language, structure, tone and pace), viewpoint and bias, how evidence
supports an argument, and comparing ideas and attitudes within one text. Terms such as connotation,
juxtaposition, rhetorical question, first-person narrator and foreshadowing are used where they fit.

Passages: a 19th-century-style scene in a mill town; the factories of the Industrial Revolution and the
Factory Acts; a narrative poem about a hiker lost in mist; how the brain learns; an inventor's failures and
success; Ibn al-Haytham and the study of light; an opinion column on solar panels for schools; a chess
tournament; Jenner and the first anaesthetics; a memoir-style account of a refugee family's arrival; a formal
letter of complaint; the deep ocean.

Non-fiction facts are limited to those taught in English schools. Written for review line by line by a
second reviewer (a teacher of KS3 English) before use.
"""

SKILLS = [
    # ------------------------------------------------------------------ RD8.01
    {
        "key": "RD8.01",
        "year": 8,
        "strand": "Stories",
        "title": "The Bell at Hollins Mill",
        "nc": "Read critically: study setting, plot and characterisation, and the effects of these",
        "text": "The bell of Hollins Mill began at half past five, as it had every morning for thirty years, and the whole of Brackley Street seemed to wake beneath it like a single tired creature. Before the bell there had been the knocker-up, old Samuel Pike, rattling his long pole against the upstairs windows; but nobody in Brackley Street truly believed the day had begun until the bell said so.\n\n"
                "Nell Ashby was eleven, and she had been a piecer for three years. She knew the bell's moods. On winter mornings it sounded cracked and impatient; in summer it was almost cheerful, as if it, too, were glad of the light. This morning, in the raw grey of March, it sounded like a summons.\n\n"
                "“Tom,” she whispered, shaking her brother's shoulder. “Up. And mind what Mother told you.”\n\n"
                "Tom was eight. He was small for eight, with a cough he had caught from the cotton dust, and he had been told, a dozen times since Sunday, that if anyone asked, he was nine.\n\n"
                "The mill swallowed them at the gate. Inside, the air was warm and wet and thick with fluff that drifted like snow that would never settle. The spinning mules ran out along the floor and back again, out and back, with a noise that was less a sound than a weather. Nell took her place among the threads, and her fingers found the broken ends and twisted them whole before her mind had quite caught up.\n\n"
                "At ten o'clock Mr Dawlish, the overlooker, came down the aisle with a stranger: a tall gentleman in a dark coat, carrying a notebook as carefully as other men carry a pocket watch.\n\n"
                "“The inspector,” said Bessie Clegg at the next frame, without moving her lips. “Come about the new law.”\n\n"
                "Nell had heard of the law in the way one hears of the sea: something vast and far away that other people had seen. Children under nine were not to work in the mills at all, people said. Children under thirteen were to work no more than nine hours a day, and to have schooling besides. It sounded, to Nell, like a story about another country.\n\n"
                "The gentleman stopped beside Tom. He bent, so that his face was level with the boy's, and Nell saw that he was not unkind; he only looked very tired, as if he had asked the same question in a hundred mills and been given the same answer.\n\n"
                "“How old are you, my lad?”\n\n"
                "Tom opened his mouth. Nell watched his lips begin to shape the lie, and watched them pause. Across the floor the mules ran out and back, out and back, as though nothing in the world could ever be altered.\n\n"
                "“I'm eight, sir,” said Tom.",
        "qs": [
            {"id": "761287866d58", "t": "text", "d": "retrieve", "q": "Find and copy the name of the job Nell has done for three years.",
             "a": ["piecer", "a piecer", "the piecer", "piecers"],
             "why": "The second paragraph says Nell “had been a piecer for three years”."},
            {"id": "16914107f75b", "t": "mcq", "d": "vocab", "q": "This morning the bell “sounded like a summons”. What is a summons?",
             "opts": ["an order to come somewhere", "a warning that danger is near", "a cry for help from far away",
                      "a friendly greeting at dawn"],
             "no": {"a warning that danger is near": "The bell is not warning of danger: it is calling the workers in to the mill, as it does every day."},
             "why": "A summons is an order to appear somewhere. The bell is calling Nell to work, and in the raw cold of March it feels like a command."},
            {"id": "8d07fc55425e", "t": "mcq", "d": "infer", "q": "Why has Tom been told to say that he is nine?",
             "opts": ["The law bans children under nine, and the family needs his work",
                      "Nine-year-olds are paid more than eight-year-olds in the mill",
                      "He is small, so the overlooker thinks he is only seven",
                      "His mother wants him to start at school a year early"],
             "why": "Nell has heard that children under nine are not to work in the mills at all, so an eight-year-old who wants to keep his place has to pretend to be nine."},
            {"id": "c05e3f0647a8", "t": "tap", "d": "language", "q": "Tap the word the writer uses to suggest the noise of the machines fills the whole room, as if it were the air itself.",
             "s": "The spinning mules ran out along the floor and back again, out and back, with a noise that was less a sound than a [weather].",
             "why": "Calling the noise “a weather” suggests it is not one sound you hear but something that fills the whole room all the time, like rain or wind."},
            {"id": "f2ae3dbc4b78", "t": "mcq", "d": "infer", "q": "Nell hears of the law “in the way one hears of the sea”. What does this comparison suggest?",
             "opts": ["It seems huge but far off, nothing to do with her life",
                      "The law frightens her, as a stormy sea would frighten her",
                      "She has studied the law in detail during her schooling",
                      "She expects the law to change her life within days"],
             "no": {"She expects the law to change her life within days": "The text says the law sounded “like a story about another country”: it does not feel real or close to her."},
             "why": "The sea is huge but far away, something “other people had seen”. The law seems the same to Nell: real somewhere, but not part of her world."},
            {"id": "3cd11fb92cf0", "t": "mcq", "d": "structure", "q": "Just before Tom answers, the writer repeats “out and back, out and back”. What is the main effect of placing it here?",
             "opts": ["It stresses the mill's endless routine just before one small change",
                      "It suggests that Tom is about to run out of the mill and back home",
                      "It explains to the reader how the spinning mules were mended each day",
                      "It shows that the inspector keeps walking up and down the long aisle"],
             "why": "The repetition, with “as though nothing in the world could ever be altered”, makes the mill seem unchangeable, so Tom's honest answer stands out as a quiet turning point."},
            {"id": "3ae32ad36cc4", "t": "mcq", "d": "summarise", "q": "Which best describes the turning point of the scene?",
             "opts": ["Tom tells the inspector the truth, not the lie he was taught",
                      "The inspector orders the mill to close for the rest of the day",
                      "Nell decides that she will leave the mill and go to school",
                      "Mr Dawlish sends Tom home because his cough is too bad"],
             "why": "Tom had been told “a dozen times” to say he was nine. The scene ends with him saying, “I'm eight, sir”: he chooses honesty."},
        ],
    },
    # ------------------------------------------------------------------ RD8.02
    {
        "key": "RD8.02",
        "year": 8,
        "strand": "Information",
        "title": "Mills, Machines and the Factory Acts",
        "nc": "Understand increasingly challenging texts: make inferences and refer to evidence in the text",
        "text": "Before the late 1700s, most cloth in Britain was made at home. A family might spin wool or cotton into thread on a spinning wheel and weave it into cloth on a hand loom, working at their own pace and selling what they made to a merchant. Within a single lifetime, that way of working was overturned.\n\n"
                "The change began with machines. Inventions such as the spinning jenny and the water frame could spin many threads at once, far faster than any person at a wheel. Early jennies were small enough to use at home, but the water frame and the larger machines that followed were too large and too expensive for a cottage, so they were gathered together in purpose-built mills. In 1771 Richard Arkwright opened a water-powered cotton mill at Cromford in Derbyshire, and it is often described as one of the first modern factories. Later, improved steam engines meant that mills no longer had to stand beside fast rivers. They could be built in towns, close to coal, canals and workers, and towns such as Manchester grew at astonishing speed.\n\n"
                "The factory brought a new kind of discipline. Workers no longer chose their own hours: they started when the bell rang and stopped when the machines stopped, often after twelve hours or more. Mill owners employed large numbers of children, partly because children could be paid far less than adults and partly because small bodies were useful. “Scavengers” crawled beneath working machines to gather loose cotton, and “piecers” leaned over the moving frames to join broken threads. Accidents were common, and the cotton dust damaged many young lungs.\n\n"
                "Not everyone accepted this as the price of progress. Doctors, writers and even some mill owners began to argue that the system was cruel, and campaigners collected evidence from the children's own accounts. Parliament responded slowly, and each law was a compromise.\n\n"
                "The Factory Act of 1833 was a turning point. It banned children under nine from working in textile mills, limited children aged nine to thirteen to nine hours a day, and said that they must receive some schooling. Most importantly, it appointed inspectors to visit mills and check that the law was obeyed. Earlier laws had failed largely because nobody enforced them. Even so, there were only four inspectors at first for the whole country, and because births were not yet officially registered, it was easy for a child to claim to be older.\n\n"
                "Further reforms followed. The Mines Act of 1842 stopped women, girls and young boys from working underground, and the Ten Hours Act of 1847 limited the working day of women and young people in textile mills. Not one of these laws ended child labour at once, but together they established an idea that now seems obvious: that the state has a duty to protect children at work, even when protecting them is less profitable.",
        "qs": [
            {"id": "67f86917698f", "t": "mcq", "d": "retrieve", "q": "According to the text, why were the new spinning machines gathered together in mills rather than used at home?",
             "opts": ["They were too large and too expensive for a cottage",
                      "Families refused to learn how to work them at home",
                      "A new law said that machines must be kept in towns",
                      "Cottages had no steam engine to drive the machines"],
             "no": {"Cottages had no steam engine to drive the machines": "Steam engines came later. The text says the machines were moved to mills because they were too large and too expensive for a cottage."},
             "why": "The second paragraph says the machines “were too large and too expensive for a cottage, so they were gathered together in purpose-built mills”."},
            {"id": "d3f2142d10cd", "t": "mcq", "d": "vocab", "q": "“The factory brought a new kind of discipline.” What does discipline mean here?",
             "opts": ["strict control over when and how people worked", "punishment given to workers who broke a machine",
                      "a subject that children studied at the mill school", "training in a skilled craft such as weaving"],
             "no": {"punishment given to workers who broke a machine": "Discipline can mean punishment, but the next sentence explains what the writer means: the bell and the machines now decided the hours."},
             "why": "The next sentence explains it: workers “no longer chose their own hours” but started and stopped when the bell and the machines did."},
            {"id": "05ff22fbc4fc", "t": "tap", "d": "retrieve", "q": "Tap the word that names the children who joined broken threads.",
             "s": "“Scavengers” crawled beneath working machines to gather loose cotton, and “[piecers]” leaned over the moving frames to join broken threads.",
             "why": "Piecers leaned over the frames to join broken threads; scavengers crawled underneath to gather loose cotton."},
            {"id": "181d7085d56a", "t": "mcq", "d": "infer", "q": "The writer says that “each law was a compromise”. What does this suggest about the reforms?",
             "opts": ["Each law gave reformers only part of what they wanted",
                      "Each law was passed quickly without any argument",
                      "Each law was written by the mill owners themselves",
                      "Each law was ignored because nobody had voted for it"],
             "why": "A compromise is a deal in which each side gives something up. The limits that follow (only four inspectors, nine hours for young children) show the laws went only part of the way."},
            {"id": "7c077fcbd652", "t": "mcq", "d": "retrieve", "q": "According to the text, why had earlier factory laws failed?",
             "opts": ["Nobody enforced them", "They covered only the mines",
                      "Children refused the schooling", "Owners had not heard of them"],
             "why": "The fifth paragraph says: “Earlier laws had failed largely because nobody enforced them.” That is why the inspectors mattered most."},
            {"id": "3ba1f53f1278", "t": "order", "d": "sequence", "q": "Put these in the order they happened, according to the text.",
             "items": ["Arkwright opens a water-powered mill at Cromford", "The first factory inspectors are appointed",
                       "Women and girls are stopped from working underground", "The Ten Hours Act limits the working day in textile mills"],
             "why": "Cromford opened in 1771; inspectors came with the Factory Act of 1833; the Mines Act was 1842; the Ten Hours Act was 1847."},
            {"id": "029a13c09d12", "t": "mcq", "d": "summarise", "q": "Which best sums up the writer's view of the reforms in the last paragraph?",
             "opts": ["They were slow and limited but set an important principle",
                      "They ended child labour in Britain almost as soon as they passed",
                      "They were a mistake that made the mills less profitable",
                      "They mattered far less than the new spinning machines"],
             "no": {"They ended child labour in Britain almost as soon as they passed": "The writer says the opposite: “Not one of these laws ended child labour at once.”"},
             "why": "The writer admits the laws did not end child labour at once, but says together they established that the state must protect children at work."},
        ],
    },
    # ------------------------------------------------------------------ RD8.03
    {
        "key": "RD8.03",
        "year": 8,
        "strand": "Poems",
        "title": "Mist on Carn Dubh",
        "nc": "Read critically: recognise a range of poetic conventions and understand how these have been used",
        "text": "At nine the sky was a held breath, blue\nfrom the car park to the summit cairn,\nand I was a quick pair of boots and a map\nfolded into a pocket I never undid.\nOnly, low in the west, a thin grey line,\nlike a pencil mark someone forgot to rub out.\n\n"
                "By noon I'd eaten my sandwiches on top\nand named every loch I could see below\nas if the view belonged to me.\nThe grey line had thickened to a wall.\nI told myself it was miles away.\nI told myself a lot of things that day.\n\n"
                "It came up the ridge the way a tide comes in:\nnot rushing, never stopping,\nfilling the hollows first, then the path,\nthen the cairn I had just left behind,\nthen my hands, held out in front of me,\npale as two strangers I'd just met.\n\n"
                "The world went small. Ten steps of heather,\none boulder shining wet, and nothing else.\nNo loch, no road, no sky. The wind\nhad dropped, and in that soft grey quiet\nmy own breath sounded far too loud,\nmy heartbeat louder still.\n\n"
                "I walked. Of course I walked. I chose\na slope that felt like down and followed it,\nfaster, then faster, until the ground\nfell suddenly away beneath one boot\nand I sat hard in the wet grass, shaking,\nat the edge of a drop I could not see the bottom of.\n\n"
                "Then, and I don't know why, I heard\nmy grandmother's voice, the one she used\nfor spilled milk and broken bones alike:\nStop. Sit. Think. Then do one thing.\nSo I stopped. I sat. I thought.\nAnd then I did one thing: I took out the map.\n\n"
                "The compass needle shivered, then lay still,\nthe one steady thing on the whole hill.\nI found the ridge, the cairn, the drop\nI'd nearly walked into, its contour lines crowded close,\nand the path I'd left, a thin dashed thread,\na long way east of where I'd thought.\n\n"
                "I blew my whistle: six long blasts,\na pause, then six again. The mist\nswallowed each note like a mouth.\nI waited, and I blew again,\nand from somewhere far below me came\nthree thin notes, answering.\n\n"
                "They found me as the light was going,\ntwo figures in red jackets, cheerful as a kitchen,\nwho said I'd done exactly right\nand walked me down between them, slowly,\nstep by careful step, along the path\nI'd been so sure I didn't need.\n\n"
                "Next morning, from the car park, Carn Dubh\nstood clear against a blameless sky,\nas if nothing had happened there at all.\nI have the map still. I have learned\nto unfold it before I need it,\nand to treat a thin grey line with respect.",
        "qs": [
            {"id": "514d8ff8d810", "t": "mcq", "d": "structure", "q": "Why does the poet include “a thin grey line” low in the west in the first verse?",
             "opts": ["It foreshadows the mist that later traps the speaker",
                      "It describes the road the speaker drove along that morning",
                      "It shows the route the speaker has drawn on the map",
                      "It suggests the summit is further away than it looks"],
             "why": "The grey line “thickened to a wall” in verse two and then came up the ridge: the small detail at the start hints at the danger to come."},
            {"id": "a2b9c23cf993", "t": "mcq", "d": "infer", "q": "In the second verse the speaker says, “I told myself a lot of things that day.” What does this line suggest?",
             "opts": ["Looking back, the speaker admits to ignoring the warnings",
                      "The speaker was talking aloud for company on the hill",
                      "The speaker was trying to recall the names of the lochs",
                      "The speaker was repeating the grandmother's advice"],
             "no": {"The speaker was talking aloud for company on the hill": "“Told myself” here means persuading oneself of something untrue: that the wall of mist was “miles away”."},
             "why": "The line before is “I told myself it was miles away.” The repetition shows the speaker, looking back, knows this was self-deception about the mist."},
            {"id": "cc677018ac0c", "t": "mcq", "d": "language", "q": "The mist “came up the ridge the way a tide comes in”. What does this comparison suggest about it?",
             "opts": ["It moved slowly but could not be stopped", "It was loud and crashed against the rocks",
                      "It was salty and cold like seawater", "It came and went again within minutes"],
             "why": "The next line explains the simile: “not rushing, never stopping”. Like a tide, the mist is steady and impossible to hold back."},
            {"id": "cb00971b9bd7", "t": "tap", "d": "language", "q": "Tap the word that suggests the speaker's own hands no longer seem to belong to the speaker.",
             "s": "pale as two [strangers] I'd just met.",
             "why": "The hands are “pale as two strangers”: in the mist even the speaker's own body looks unfamiliar, which shows how disorientated the speaker has become."},
            {"id": "c8348bacc0c2", "t": "text", "d": "retrieve", "q": "After remembering the grandmother's words, the speaker does “one thing”. Find and copy the object the speaker takes out.",
             "a": ["the map", "map", "a map"],
             "why": "Verse six ends: “And then I did one thing: I took out the map.”"},
            {"id": "b92cbe44ac42", "t": "mcq", "d": "compare", "q": "How does the speaker's behaviour change after hearing the grandmother's voice?",
             "opts": ["From hurrying blindly to acting calmly, step by step",
                      "From calm planning to panic as the mist gets thicker",
                      "From walking slowly to running to find the path",
                      "From reading the map to trusting gut feelings instead"],
             "no": {"From reading the map to trusting gut feelings instead": "It is the other way round: before, the speaker follows “a slope that felt like down”; afterwards, the speaker uses the map and compass."},
             "why": "Before, the speaker walks “faster, then faster” on a guess and nearly falls; afterwards the speaker stops, sits, thinks, and uses the map, compass and whistle."},
            {"id": "2ae31d67f355", "t": "mcq", "d": "summarise", "q": "Which best sums up the lesson the speaker takes from the day, in the last verse?",
             "opts": ["Prepare before trouble comes, and heed warning signs",
                      "Never walk in the hills alone, even in fine weather",
                      "Mountain rescue teams will always find a lost walker",
                      "A clear morning sky means the whole day will be safe"],
             "why": "The speaker has learned “to unfold it before I need it” and “to treat a thin grey line with respect”: to be ready, and to heed early warnings."},
        ],
    },
    # ------------------------------------------------------------------ RD8.04
    {
        "key": "RD8.04",
        "year": 8,
        "strand": "Explanations",
        "title": "How the Brain Learns",
        "nc": "Understand increasingly challenging texts: know the purpose, audience for and context of the writing",
        "text": "Every time you learn something new, whether it is a French verb, a football skill or the route to a friend's house, your brain physically changes. Understanding how that happens can make you a far more effective learner.\n\n"
                "The brain is made of billions of nerve cells called neurons. Each neuron is linked to many others at tiny junctions called synapses, where signals pass from one cell to the next. When you think, remember or move, chains of neurons send signals along particular pathways. Learning is the process of building and strengthening those pathways.\n\n"
                "Imagine walking across a field of long grass. The first time, it is hard going and you leave hardly a trace. If you walk the same way every day, a path appears, and soon it is quick and easy to follow. Pathways in the brain behave in a similar way. The first time you try to remember a fact, the connection is weak. Each time you use it, the synapses involved become more efficient, and the signal travels more easily. Scientists sometimes sum this up in a short phrase: neurons that fire together, wire together.\n\n"
                "This explains a surprising finding. Rereading your notes feels productive, because the words look familiar, but familiarity is not the same as memory. A far stronger method is retrieval practice: closing the book and trying to recall the information, for example by answering questions or writing down everything you can remember. The effort of searching for an answer is what strengthens the pathway. Getting an answer wrong and then checking it can help too, as long as you correct the mistake.\n\n"
                "Timing matters as well. In the 1880s the German psychologist Hermann Ebbinghaus tested his own memory of lists of made-up syllables and found that he forgot much of what he had learned within a day or two. However, each time he relearned the material, he forgot it more slowly. This is why spacing your practice, returning to a topic after a day, then a week, then a month, works better than cramming it all into one evening.\n\n"
                "Finally, the brain does some of its most important work when you are not studying at all. During sleep, the brain replays and sorts the day's experiences, and new memories become more stable. A pupil who stays up late to revise and then sleeps badly may be throwing away much of the benefit.\n\n"
                "Not one part of this means that learning should feel easy. In fact, the opposite is closer to the truth. When practice feels like a struggle, it is often because your brain is doing exactly the work that makes memories last.",
        "qs": [
            {"id": "3fe925de84eb", "t": "mcq", "d": "retrieve", "q": "According to the text, what are synapses?",
             "opts": ["tiny junctions where signals pass between cells", "the billions of nerve cells that make up the brain",
                      "pathways that form when we walk the same way", "memories that have become stable during sleep"],
             "no": {"the billions of nerve cells that make up the brain": "Those are neurons. Synapses are the junctions between them."},
             "why": "The second paragraph says neurons are linked “at tiny junctions called synapses, where signals pass from one cell to the next”."},
            {"id": "a78220b93d5f", "t": "mcq", "d": "language", "q": "Why does the writer ask the reader to imagine walking across a field of long grass?",
             "opts": ["To give a familiar picture of how practice strengthens a pathway",
                      "To suggest that walking outdoors helps people to remember facts",
                      "To describe the place where Ebbinghaus carried out his tests",
                      "To show that learning is slow and that most people give up"],
             "why": "The writer says pathways in the brain “behave in a similar way”: the analogy turns an invisible process into something the reader can picture."},
            {"id": "bff465e9763e", "t": "mcq", "d": "compare", "q": "How does the writer compare rereading notes with retrieval practice?",
             "opts": ["Rereading feels useful but works less well than effortful retrieval",
                      "Rereading is faster and works just as well, so retrieval is a waste of time",
                      "Retrieval is only useful for facts, while rereading is better for skills",
                      "Both work equally well, as long as the pupil sleeps well afterwards"],
             "why": "Rereading “feels productive” because the words look familiar, but “familiarity is not the same as memory”; retrieval is “a far stronger method” because of the effort involved."},
            {"id": "a06501512dd5", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you what Ebbinghaus put in his lists.",
             "s": "In the 1880s the German psychologist Hermann Ebbinghaus tested his own memory of lists of made-up [syllables] and found that he forgot much of what he had learned within a day or two.",
             "why": "He tested himself on lists of made-up syllables, so his results could not be helped by words he already knew."},
            {"id": "82d9b2978f3c", "t": "mcq", "d": "vocab", "q": "The writer warns against “cramming it all into one evening”. What does cramming mean here?",
             "opts": ["trying to learn a lot in one short burst", "copying notes out neatly in full sentences",
                      "revising together with a group of friends", "testing yourself with questions and answers"],
             "no": {"testing yourself with questions and answers": "That is retrieval practice, which the writer recommends. Cramming is squeezing the learning into one session."},
             "why": "The writer contrasts cramming with “spacing your practice” over days and weeks, so cramming means squeezing it all into one short session."},
            {"id": "3c20e31225b9", "t": "mcq", "d": "infer", "q": "A pupil has a science test in three weeks. Which plan would the writer most recommend?",
             "opts": ["Short self-quizzes spread over the three weeks, with plenty of sleep",
                      "Rereading the notes carefully every evening in the final week",
                      "One long revision session late on the night before the test",
                      "Copying out all the notes neatly once, then resting until the test"],
             "why": "The plan combines all three of the writer's points: retrieval practice, spacing over time, and sleep. The others rely on rereading, cramming or late nights."},
            {"id": "552579a078b5", "t": "mcq", "d": "purpose", "q": "What is the main purpose of the text?",
             "opts": ["To explain how learning works so that readers can study better",
                      "To tell the life story of the scientist Hermann Ebbinghaus",
                      "To persuade schools to start their lessons later in the day",
                      "To describe the illnesses that can damage the human brain"],
             "why": "It explains neurons, retrieval, spacing and sleep, and keeps turning to “you”: the aim is to help the reader become “a far more effective learner”."},
        ],
    },
    # ------------------------------------------------------------------ RD8.05
    {
        "key": "RD8.05",
        "year": 8,
        "strand": "Stories",
        "title": "The Seventh Spoon",
        "nc": "Read critically: know how language, vocabulary choice and text structure present meaning",
        "text": "The first spoon was a disaster, and I knew it before Avô even lifted it.\n\n"
                "I had made it from a soup spoon, a lump of modelling clay and about forty coins taped into a fat handle. The idea was simple: if the spoon were heavy enough, his hand would not be able to shake it. Avô held it as if it were a gift, which in a way it was, and dipped it into his bowl of soup. The spoon did not shake. Instead, his whole arm did, slowly, under the weight, and the soup slid back into the bowl before it was halfway to his mouth.\n\n"
                "“A very strong spoon,” he said gravely. “Good for building houses.”\n\n"
                "Avô had been a carpenter in Porto for forty years. His hands had made staircases and window frames and the cradle I slept in as a baby. Now they trembled so badly that he had started eating alone in the kitchen, after the rest of us had finished, so that nobody would see.\n\n"
                "Spoons two to five lived in a shoebox under my bed, which my brother Rui called the Museum of Failure. Number two had a handle so thick that Avô could not close his fingers around it. Number three had a hinge that was meant to swing and absorb the shaking; instead it swung and flung peas across the kitchen. Number four snapped. Number five worked beautifully, as long as nobody tried to eat anything with it.\n\n"
                "By number six I had stopped trying to defeat the tremor and started trying to understand it. I watched videos from university laboratories. I read about engineers who do not fight a shake at all, but measure it and move against it, cancelling it out. That was far beyond anything I could build in a bedroom. But I noticed something else: Avô's shake was worst when he gripped tightly, and gentler when his arm rested on something.\n\n"
                "So spoon number seven was not really a spoon. It was a wide wooden block that sat on the table, with a smooth groove along the top. Avô rested his forearm in the groove, and the spoon, fixed to a short lever, could only move one way: up towards his mouth, and down again. It was ugly. It was made from offcuts of pine and the wheel of an old skateboard. Rui said it looked like a tiny catapult.\n\n"
                "On Sunday Avô sat at the table with the rest of us. He laid his arm in the groove. He was concentrating so hard that nobody spoke. The spoon rose, trembling only slightly, and arrived.\n\n"
                "He ate the whole bowl. Then he turned the block over in his big, unsteady hands, ran a thumb along the joint I had glued, and frowned.\n\n"
                "“The sanding is bad,” he said. “Tomorrow, I will show you how.”",
        "qs": [
            {"id": "6eb7aa2f07eb", "t": "mcq", "d": "infer", "q": "When Avô calls the first spoon “Good for building houses”, what does this show about him?",
             "opts": ["He uses gentle humour so the failure does not hurt",
                      "He thinks the narrator should become a builder",
                      "He is angry that the spoon has spilled his soup",
                      "He wants to use the coins for a building project"],
             "why": "He holds the spoon “as if it were a gift” and makes a joke about its weight: he is being kind about a spoon that clearly does not work."},
            {"id": "cc043b0a64cb", "t": "mcq", "d": "language", "q": "Why does the narrator tell us that Avô's hands once made staircases, window frames and a cradle?",
             "opts": ["To contrast his skilled past with his struggle in the present",
                      "To explain where the narrator found the wood for the seventh spoon",
                      "To show that Avô still works as a carpenter in Porto every day",
                      "To suggest that Avô's tremor was caused by years of hard work"],
             "no": {"To suggest that Avô's tremor was caused by years of hard work": "The text never says what caused the tremor. The list is there to show what his hands could do before."},
             "why": "The next sentence begins “Now they trembled”: setting the skilled hands of the past beside the shaking hands of the present shows how much he has lost."},
            {"id": "0eee3872edcc", "t": "mcq", "d": "infer", "q": "What does Avô's habit of eating after everyone else suggest about how he feels?",
             "opts": ["He is ashamed of his shaking hands", "He simply prefers to eat in silence",
                      "He is too busy to eat with the family", "He does not like the family's cooking"],
             "no": {"He simply prefers to eat in silence": "The text gives the reason: he eats alone “so that nobody would see”. That is about hiding, not about liking quiet."},
             "why": "He eats alone so that nobody sees him tremble, which suggests embarrassment. That is why it matters so much that, at the end, he sits “with the rest of us”."},
            {"id": "746871ea5495", "t": "mcq", "d": "vocab", "q": "Spoon number three had a hinge “meant to swing and absorb the shaking”. What does absorb mean here?",
             "opts": ["take in and reduce", "make much stronger", "measure and record", "copy and repeat"],
             "why": "The hinge was meant to soak up the shaking so the spoon stayed still, though in fact it “flung peas across the kitchen”."},
            {"id": "9d494564c5c2", "t": "tap", "d": "structure", "q": "Tap the two words that show what the narrator first tried to do to the tremor, and what the narrator tried to do instead.",
             "s": "By number six I had stopped trying to [defeat] the tremor and started trying to [understand] it.",
             "why": "The narrator stops trying to defeat (overpower) the tremor and starts trying to understand it. This sentence is the turning point that leads to spoon seven."},
            {"id": "eeb468e89454", "t": "order", "d": "sequence", "q": "Put the narrator's designs in the order they were made.",
             "items": ["A spoon with a heavy handle full of coins", "A spoon with a handle too thick to hold",
                       "A spoon with a hinge that flung peas", "A wooden block with a groove for the forearm"],
             "why": "The coin spoon was first, the thick handle number two, the hinge number three, and the wooden block number seven."},
            {"id": "93cd17340606", "t": "mcq", "d": "infer", "q": "At the end, Avô frowns and says, “The sanding is bad. Tomorrow, I will show you how.” What does this suggest?",
             "opts": ["He values the invention and, as a craftsman, wants to improve it",
                      "He is disappointed because the invention has not really worked",
                      "He thinks the narrator should give up and leave it to him",
                      "He is annoyed that the narrator used his wood without asking"],
             "no": {"He is disappointed because the invention has not really worked": "It has worked: “He ate the whole bowl.” His frown is a carpenter judging the finish, not the idea."},
             "why": "He has just eaten a whole bowl. His comment shows him taking the work seriously, as one maker to another, and offering to teach: a quiet sign of pride and respect."},
        ],
    },
    # ------------------------------------------------------------------ RD8.06
    {
        "key": "RD8.06",
        "year": 8,
        "strand": "Biography",
        "title": "Ibn al-Haytham and the Science of Seeing",
        "nc": "Understand increasingly challenging texts: make inferences and refer to evidence in the text",
        "text": "For more than a thousand years, some of the greatest thinkers of the ancient world believed that we see because our eyes send something out. According to this idea, rays travel from the eye towards an object, like invisible fingers feeling their way across a room. It seemed reasonable. It was also wrong, and one of the people who did most to show why was a scholar named Ibn al-Haytham.\n\n"
                "Ibn al-Haytham was born in about 965 in Basra, in what is now Iraq, and later worked in Cairo, in Egypt. He lived at a time when scholars in cities such as Baghdad and Cairo were translating, studying and arguing over the works of Greek writers, and adding a great deal of their own. He wrote on mathematics, astronomy and many other subjects, but he is best remembered for his work on light and vision, gathered in a long work known as the Book of Optics.\n\n"
                "His central argument was simple to state. We see an object, he said, because light travels from it into our eyes, not the other way round. A very bright light hurts the eye, he pointed out, and an afterimage can linger after you look away: both suggest that something is entering the eye from outside, rather than leaving it.\n\n"
                "What made his work remarkable, however, was not only what he concluded but how he reached it. Ibn al-Haytham did not simply accept an idea because a famous writer had held it. He insisted that a claim should be tested by careful observation and by experiments that others could repeat. He wrote that a person who studies the works of scientists should make himself an enemy of everything he reads, questioning it from every side, and should be suspicious of his own judgement too.\n\n"
                "One of his best-known investigations used a darkened room with a small hole in one wall. Light from the bright scene outside passed through the hole and formed an image on the opposite wall, upside down. He showed that light travels in straight lines, which is why the image is inverted. This arrangement, later called a camera obscura, Latin for “dark room”, is the forerunner of the modern camera.\n\n"
                "His Book of Optics was translated into Latin, and European scholars studied it for centuries. In 2015, when the United Nations held an International Year of Light, his work was celebrated as part of it, roughly a thousand years after he wrote it.\n\n"
                "Today we take it for granted that a scientific idea must earn its place through evidence. Ibn al-Haytham is one of the reasons we do.",
        "qs": [
            {"id": "225d658d5279", "t": "mcq", "d": "language", "q": "The old theory is described as rays “like invisible fingers feeling their way across a room”. What is the effect of this simile?",
             "opts": ["It helps the reader picture the eye reaching out to touch things",
                      "It suggests the old theory was dangerous to the people who held it",
                      "It shows that the ancient thinkers had studied the human hand",
                      "It shows that the writer still believes the old theory of sight"],
             "why": "The simile turns an abstract idea into a picture: the eye sending out something that gropes towards objects, as fingers do in the dark."},
            {"id": "d85d93613641", "t": "mcq", "d": "structure", "q": "The first paragraph includes two short sentences: “It seemed reasonable. It was also wrong.” What is their main effect?",
             "opts": ["They set up a sharp contrast that hooks the reader into the account",
                      "They slow the text down to describe the old theory in detail",
                      "They tell the reader that Ibn al-Haytham agreed with the old theory",
                      "They show that the writer is unsure which theory is correct"],
             "why": "Two short, balanced sentences turn suddenly from “reasonable” to “wrong”, which surprises the reader and leads straight into who proved it wrong."},
            {"id": "f2433060c115", "t": "text", "d": "retrieve", "q": "Find and copy the name of the city where Ibn al-Haytham was born.",
             "a": ["Basra"],
             "why": "The second paragraph says he “was born in about 965 in Basra, in what is now Iraq”. He later worked in Cairo."},
            {"id": "428e9c33e5aa", "t": "mcq", "d": "retrieve", "q": "Which piece of evidence did Ibn al-Haytham use to support his argument about vision?",
             "opts": ["A very bright light hurts the eye", "The eye can see in total darkness",
                      "Rays can be seen leaving the eye", "Light bends as it enters water"],
             "no": {"Rays can be seen leaving the eye": "That would support the old theory, and the text never says it. He argued the opposite: something enters the eye."},
             "why": "The third paragraph says a bright light hurts the eye and an afterimage lingers, which suggests something is entering the eye from outside."},
            {"id": "93fd2425b160", "t": "mcq", "d": "infer", "q": "He said a reader of scientists' works should make himself “an enemy of everything he reads”. What attitude does this show?",
             "opts": ["Every claim should be tested, however famous its author",
                      "Scientists' books are harmful and should not be read at all",
                      "Scholars should argue fiercely with one another in public",
                      "Only ideas from his own time could be trusted as true"],
             "no": {"Scientists' books are harmful and should not be read at all": "He wants the books read, but read critically: “questioning it from every side”."},
             "why": "He did not accept an idea “because a famous writer had held it”; being an “enemy” of a text means questioning it from every side, and doubting yourself too."},
            {"id": "97831cc5ec6e", "t": "tap", "d": "vocab", "q": "Tap the word that means “upside down”.",
             "s": "He showed that light travels in straight lines, which is why the image is [inverted].",
             "why": "Inverted means turned upside down: the sentence before says the image formed on the wall “upside down”."},
            {"id": "3de63b6ef744", "t": "mcq", "d": "purpose", "q": "What does the writer present as the most important part of Ibn al-Haytham's legacy?",
             "opts": ["He showed ideas must be tested through careful experiments",
                      "He invented the modern camera in a darkened room in Cairo",
                      "He translated the works of the Greek writers into Arabic",
                      "The United Nations named an International Year after him"],
             "no": {"He invented the modern camera in a darkened room in Cairo": "The text calls the camera obscura “the forerunner of the modern camera”, not the camera itself, and stresses his method above any single result."},
             "why": "The writer says what was remarkable was “not only what he concluded but how he reached it”, and ends: a scientific idea “must earn its place through evidence”."},
        ],
    },
    # ------------------------------------------------------------------ RD8.07
    {
        "key": "RD8.07",
        "year": 8,
        "strand": "Persuasive writing",
        "title": "Our Schools Are Sitting in the Sun",
        "nc": "Read critically: know how language, including figurative language, vocabulary choice and text structure, presents meaning",
        "text": "Walk past almost any secondary school on a bright afternoon and look up. What do you see? Acres of flat grey roof, baking quietly in the sunshine, doing absolutely nothing. I find it hard to think of a bigger missed opportunity in British education.\n\n"
                "Schools are, in many ways, perfect places for solar panels. They have large, flat roofs. They use most of their electricity during daylight hours, which is exactly when panels generate it. And unlike a family, a school is not going to move house in five years' time. A panel fitted this summer could still be quietly producing electricity when this year's Year 7s bring their own children to parents' evening.\n\n"
                "The objections are familiar, and they are weaker than they sound. “Britain is too cloudy,” people say. Yet solar panels still generate electricity on overcast days, though less than in bright sun, and Germany, hardly a land of endless sunshine, has built a great deal of solar power. “It costs too much,” say others. It is true that panels are expensive to install. But they need no fuel, and over their lifetime they can save a school a large share of what it spends on electricity: money that could pay for books, trips and teachers instead.\n\n"
                "Then there is the lesson itself. Last term I visited a primary school in Norfolk that had covered its hall roof with panels. In the entrance, a screen showed how much electricity the roof was producing at that moment. A boy of about eight, Ravi, dragged me over to it. “Look,” he said, pointing. “When the cloud goes over, the number drops.” He had grasped, without being told, something that many adults never think about: that energy comes from somewhere, and that the somewhere matters.\n\n"
                "How many science lessons could be built around that one screen? How many children would leave school understanding, not just memorising, where their electricity comes from?\n\n"
                "Of course, solar panels alone will not solve every energy problem. The sun sets, and electricity is needed at night and through the dark months of winter. Panels must be part of a mix that includes wind power, ways of storing energy, and simply using less in the first place. But that is an argument for doing more, not for doing nothing.\n\n"
                "Every year we wait is another year of sunlight falling, uselessly, on school roofs. It is time we looked up.",
        "qs": [
            {"id": "068a86096445", "t": "mcq", "d": "language", "q": "The column opens with a rhetorical question: “What do you see?” Why does the writer use it?",
             "opts": ["To make readers picture the empty roofs for themselves",
                      "To find out what readers think about school buildings",
                      "To show that the writer is unsure what is on the roofs",
                      "To ask readers to write in with their own answers"],
             "why": "A rhetorical question does not expect a reply. Here it pulls the reader into the scene so they “see” the wasted roofs, which the writer then describes."},
            {"id": "a3b3fb2f5f0e", "t": "mcq", "d": "retrieve", "q": "Which reason does the writer give for schools being “perfect places for solar panels”?",
             "opts": ["They use most of their electricity in daylight", "They are empty for the whole summer holiday",
                      "Their pupils can keep the panels clean", "They have no other way of getting power"],
             "no": {"They are empty for the whole summer holiday": "The writer never mentions holidays, and that would be a weakness, not a strength: the point is that schools use power when the sun shines."},
             "why": "The second paragraph says schools “use most of their electricity during daylight hours, which is exactly when panels generate it”."},
            {"id": "8b5acf918f5c", "t": "mcq", "d": "structure", "q": "How does the writer organise the third paragraph?",
             "opts": ["Each objection is quoted, then answered with a counter-argument",
                      "Both sides are described equally, with no conclusion drawn",
                      "The writer lists facts about panels in the order they were invented",
                      "The writer tells a story about an argument with a head teacher"],
             "why": "The writer quotes “Britain is too cloudy” and “It costs too much” and answers each one in turn: a counter-argument structure."},
            {"id": "73250f7a08c8", "t": "tap", "d": "vocab", "q": "Tap the word that means “covered with cloud”.",
             "s": "Yet solar panels still generate electricity on [overcast] days, though less than in bright sun, and Germany, hardly a land of endless sunshine, has built a great deal of solar power.",
             "why": "Overcast days are cloudy ones. The writer is answering the objection that “Britain is too cloudy”."},
            {"id": "67b907f2b2fb", "t": "mcq", "d": "purpose", "q": "Why does the writer include the story of Ravi at the school in Norfolk?",
             "opts": ["To show, through a real child, what pupils can learn from the panels",
                      "To prove that panels produce more power in Norfolk than elsewhere",
                      "To suggest that primary schools need panels more than secondaries",
                      "To show that young children find solar panels hard to understand"],
             "no": {"To show that young children find solar panels hard to understand": "The reverse: Ravi “had grasped, without being told” how the panels respond to cloud."},
             "why": "The anecdote supports the point that panels are a “lesson”: a vivid example of a child understanding where energy comes from."},
            {"id": "4743e07b4a3a", "t": "mcq", "d": "infer", "q": "In the second-to-last paragraph the writer admits that solar panels “alone will not solve every energy problem”. Why include this?",
             "opts": ["To seem fair, then turn the weakness into a reason to do more",
                      "To show that the writer has changed their mind about solar power",
                      "To persuade readers that wind power is better than solar power",
                      "To explain how solar panels store electricity for the night"],
             "why": "Admitting a limit makes the writer sound reasonable, and the paragraph ends by turning it round: “an argument for doing more, not for doing nothing”."},
            {"id": "819de1ead9eb", "t": "mcq", "d": "purpose", "q": "Which of these sentences from the column is an opinion rather than a fact?",
             "opts": ["I find it hard to think of a bigger missed opportunity in British education.",
                      "It is true that panels are expensive to install.",
                      "The sun sets, and electricity is needed at night and through the dark months of winter.",
                      "In the entrance, a screen showed how much electricity the roof was producing at that moment."],
             "why": "Whether this is the “biggest missed opportunity” is the writer's personal judgement and cannot be proved. The others can be checked."},
        ],
    },
    # ------------------------------------------------------------------ RD8.08
    {
        "key": "RD8.08",
        "year": 8,
        "strand": "Stories",
        "title": "Board One",
        "nc": "Read critically: study setting, plot and characterisation, and the effects of these",
        "text": "Before the last round, Mr Osei had told Farah only one thing. “When you are winning,” he said, “sit on your hands.”\n\n"
                "She had laughed. She was twelve, and she had never been winning against anyone like Tomasz Nowak.\n\n"
                "The hall of the Leicester Junior Congress smelled of floor polish and orange squash. Sixty boards were laid out in long rows, and on each one a clock ticked quietly beside the pieces, like a small, impatient heart. Farah was on board one. She had reached it by winning four games she had expected to lose, and she still half believed that somebody would come over and tell her there had been a mistake.\n\n"
                "Tomasz was fifteen and the top seed. He shook her hand without looking at her, pressed his clock, and played his first move as if it bored him.\n\n"
                "For two hours nothing happened, which in chess means that everything happened. Pieces moved forward and back. Pawns locked together in the centre. Farah's knees jiggled under the table, and twice she had to stop herself from chewing the sleeve of her jumper. Then, on move thirty-one, Tomasz made a small mistake: a bishop placed one square too far from home. Farah saw it, and the whole hall seemed to tilt.\n\n"
                "Three moves later she had won a rook. She could feel the win now, warm and close, like the smell of bread from an oven. Her hand reached for her queen. One check, then another, and he would have to resign.\n\n"
                "Sit on your hands.\n\n"
                "She took her hand back and, feeling slightly foolish, actually tucked it under her leg. And while it was there, trapped and useless, she looked at her own side of the board for the first time in twenty minutes. Her king sat on its starting square behind three loyal pawns. Tomasz's rook stood on the open file, waiting. Her queen was the only piece guarding her back row. If it went chasing his king and the checks ran out, his rook would drop onto that row, and her king, hemmed in by its own pawns, would be checkmated. Her own pawns would have been the walls of her prison.\n\n"
                "Farah breathed out. She pushed one pawn forward a single square, giving her king room to escape. It was the quietest, dullest move on the board.\n\n"
                "Tomasz looked at it for a long time. Then, for the first time all afternoon, he looked up at her. He tipped his king over gently and held out his hand.\n\n"
                "“That was the right move,” he said. “Most people play the check.”\n\n"
                "Afterwards, Mr Osei did not say well done. He just asked her, with a small smile, where her hands had been.",
        "qs": [
            {"id": "dc86cf89162d", "t": "mcq", "d": "structure", "q": "Why does the writer open the story with Mr Osei's advice, “sit on your hands”?",
             "opts": ["It foreshadows the moment when the advice saves her game",
                      "It shows that Mr Osei thinks Farah cannot possibly win",
                      "It explains the rules of the tournament to the reader",
                      "It suggests Farah's hands are cold in the chess hall"],
             "why": "The advice seems a joke at first (“She had laughed”), but it returns in its own short paragraph at the key moment and stops her playing the losing check."},
            {"id": "02045c52c5af", "t": "mcq", "d": "language", "q": "Each clock ticks “like a small, impatient heart”. What does this simile add to the setting?",
             "opts": ["A sense of tension and of time pressing on the players",
                      "A sense that the hall is warm, calm and comfortable",
                      "A hint that one of the players is about to fall ill",
                      "A suggestion that the clocks are old and unreliable"],
             "why": "A heartbeat suggests nerves, and “impatient” suggests time running out: the simile builds the tension of the final round."},
            {"id": "18d06322998c", "t": "mcq", "d": "retrieve", "q": "According to the text, how had Farah reached board one?",
             "opts": ["By winning four games she had expected to lose", "By being named the top seed before the event",
                      "By beating Tomasz Nowak in an earlier round", "By being chosen by Mr Osei to play there"],
             "no": {"By being named the top seed before the event": "Tomasz is the top seed. Farah reached board one through her results."},
             "why": "The third paragraph says she “had reached it by winning four games she had expected to lose”."},
            {"id": "cccdd949c97a", "t": "mcq", "d": "infer", "q": "What do Tomasz's actions at the start of the game suggest about his attitude to Farah?",
             "opts": ["He does not take her seriously as an opponent", "He is too nervous to look at her",
                      "He is annoyed that the game has started late", "He has decided to let her win the game"],
             "no": {"He is too nervous to look at her": "Nothing suggests nerves: he plays his first move “as if it bored him”. Not looking at her suggests he dismisses her."},
             "why": "He shakes her hand “without looking at her” and plays “as if it bored him”: he expects an easy win against a younger, lower-ranked player."},
            {"id": "22f1e67a63b4", "t": "mcq", "d": "vocab", "q": "“One check, then another, and he would have to resign.” What does resign mean in this sentence?",
             "opts": ["give up the game, admitting defeat", "leave the chess club for good",
                      "ask for the game to be started again", "sign the score sheet at the end"],
             "why": "In chess, a player who resigns gives up the game before checkmate. Tomasz does this at the end by tipping his king over."},
            {"id": "c918486e0176", "t": "tap", "d": "language", "q": "Tap the word that names the place the writer compares Farah's trapped king to.",
             "s": "Her own pawns would have been the walls of her [prison].",
             "why": "The metaphor turns her “loyal” pawns into prison walls: the pieces meant to protect her king would have stopped it escaping."},
            {"id": "032f18650e85", "t": "mcq", "d": "compare", "q": "How does Tomasz's attitude to Farah at the end of the game compare with his attitude at the start?",
             "opts": ["He moves from dismissing her to respecting her",
                      "He moves from respecting her to resenting her",
                      "He is just as bored at the end as at the start",
                      "He moves from friendliness to cold anger"],
             "no": {"He moves from respecting her to resenting her": "It is the other way round: at the start he will not look at her; at the end he looks up, shakes her hand and praises her move."},
             "why": "At the start he will not look at her; at the end he looks up “for the first time all afternoon”, resigns gently and praises her move."},
        ],
    },
    # ------------------------------------------------------------------ RD8.09
    {
        "key": "RD8.09",
        "year": 8,
        "strand": "Information",
        "title": "Two Turning Points in Medicine",
        "nc": "Understand increasingly challenging texts: make inferences and refer to evidence in the text",
        "text": "Two hundred and fifty years ago, a visit to the surgeon was something to be dreaded, and smallpox was one of the most feared diseases in the world. Within a single century, two discoveries changed both of these facts, and they still shape the medicine we rely on today.\n\n"
                "Smallpox spread easily from person to person. It killed many of those who caught it, and it left many survivors with deep scars or blindness. In the 1700s, some people tried to protect themselves by deliberately catching a mild dose of smallpox, a risky method that could still kill.\n\n"
                "Edward Jenner, a doctor in the village of Berkeley in Gloucestershire, had heard a local belief: milkmaids who caught cowpox, a mild disease of cattle, did not seem to catch smallpox. In 1796 he decided to test it. He took material from a cowpox sore on the hand of a milkmaid, Sarah Nelmes, and put it into small cuts on the arm of James Phipps, the eight-year-old son of his gardener. James became slightly unwell, then recovered. Weeks later, Jenner exposed him to smallpox. James did not catch it.\n\n"
                "Today Jenner's experiment would never be allowed, because it put a child at serious risk without the safeguards we now expect. But it worked, and Jenner went on to test the method on others and to publish his results. His method was called vaccination, from vacca, the Latin word for cow. In 1980, after a long worldwide campaign of vaccination, smallpox was declared eradicated: the first human disease ever to be wiped out.\n\n"
                "The second breakthrough came from a different problem: pain. Before the 1840s, surgery was performed on patients who were wide awake. Speed was everything, and the best surgeons were praised for how quickly they could work. Many people refused operations that might have saved them, preferring the illness to the knife.\n\n"
                "In 1846, at a hospital in Boston in the United States, a dentist named William Morton gave a patient ether to breathe before an operation. The patient slept through it. The news crossed the Atlantic within a couple of months. A year later, in Edinburgh, the doctor James Young Simpson began using chloroform, which was easier to handle. Anaesthetics meant that surgeons could at last work slowly and carefully, and attempt operations that had been impossible before.\n\n"
                "Neither discovery made medicine safe at once. Anaesthetics carried their own dangers, and many patients still died from infections after surgery until doctors learned to keep wounds and instruments clean. Yet together, vaccination and anaesthesia show two great habits of modern medicine: looking carefully at what is in front of you, and refusing to accept that suffering is simply the way things are.",
        "qs": [
            {"id": "ec18143203a4", "t": "mcq", "d": "retrieve", "q": "What local belief did Jenner decide to test?",
             "opts": ["Milkmaids who caught cowpox did not seem to catch smallpox",
                      "Catching a mild dose of smallpox protected people from it",
                      "Cowpox spread easily from cattle to every farm worker",
                      "Children who lived on farms never caught any disease"],
             "no": {"Catching a mild dose of smallpox protected people from it": "That was the older, risky method described in the second paragraph. Jenner's idea was about cowpox."},
             "why": "The third paragraph says he had heard that “milkmaids who caught cowpox, a mild disease of cattle, did not seem to catch smallpox”."},
            {"id": "d9faabe33e08", "t": "order", "d": "sequence", "q": "Put the steps of Jenner's experiment in order.",
             "items": ["Jenner takes material from a cowpox sore on Sarah Nelmes's hand", "The material is put into small cuts on James Phipps's arm",
                       "James becomes slightly unwell, then recovers", "Jenner exposes James to smallpox"],
             "why": "The third paragraph gives the steps in this order, ending: “Weeks later, Jenner exposed him to smallpox. James did not catch it.”"},
            {"id": "0cdfcca691d8", "t": "text", "d": "retrieve", "q": "Find and copy the Latin word that the word vaccination comes from.",
             "a": ["vacca"],
             "why": "The fourth paragraph says vaccination comes “from vacca, the Latin word for cow”."},
            {"id": "aea7b22e81fd", "t": "mcq", "d": "infer", "q": "What is the writer's attitude to Jenner's experiment in the fourth paragraph?",
             "opts": ["Critical of the risk to a child, but clear that it worked",
                      "Fully approving, since it was the safest test possible",
                      "Angry, arguing that it should never have been published",
                      "Doubtful about whether the experiment really worked"],
             "why": "The writer says it “would never be allowed” today because of the risk to a child, then turns with “But it worked”: a balanced view."},
            {"id": "40d396f3f66e", "t": "mcq", "d": "infer", "q": "Many people preferred “the illness to the knife”. What does this suggest about surgery before anaesthetics?",
             "opts": ["Its pain was so terrible that some would rather risk dying",
                      "Surgeons were too few for most people to reach one in time",
                      "Operations cost far more money than most families had",
                      "Doctors usually advised patients to avoid any operation"],
             "why": "Patients were “wide awake” during surgery. Choosing a possibly fatal illness over an operation shows how dreadful the pain of surgery was."},
            {"id": "9ff1e1bce451", "t": "mcq", "d": "structure", "q": "How is the text organised?",
             "opts": ["It explains one breakthrough, then another, then links them",
                      "It compares the two discoveries point by point in every paragraph",
                      "It tells the life story of Edward Jenner from his birth to his death",
                      "It argues for vaccination first, then argues against anaesthetics"],
             "why": "Paragraphs two to four cover vaccination, paragraphs five and six anaesthetics, and the last paragraph draws them together."},
            {"id": "8cd4f295300f", "t": "mcq", "d": "compare", "q": "According to the final paragraph, what do the two discoveries have in common?",
             "opts": ["Both show careful observation and a refusal to accept suffering",
                      "Both made medicine completely safe as soon as they were found",
                      "Both were first tried in hospitals in the United States",
                      "Both were discovered by dentists working in Edinburgh"],
             "no": {"Both made medicine completely safe as soon as they were found": "The writer says the opposite: “Neither discovery made medicine safe at once.”"},
             "why": "The writer says they show two habits: “looking carefully at what is in front of you, and refusing to accept that suffering is simply the way things are”."},
        ],
    },
    # ------------------------------------------------------------------ RD8.10
    {
        "key": "RD8.10",
        "year": 8,
        "strand": "Biography",
        "title": "The Coat in the Suitcase",
        "nc": "Read a wide range of non-fiction, including autobiography: make inferences and refer to evidence in the text",
        "text": "I was ten when we arrived in Cardiff, and the first thing I noticed was that the rain did not stop. In the city we had left, rain was an event. People ran out into the first storm of autumn and turned their faces up to it. In Cardiff, it seemed, rain was simply the air.\n\n"
                "We came with two suitcases and a plastic bag. My father carried the heavier case, which held our clothes, four cooking pots and his teaching certificates, wrapped in a towel as carefully as if they were made of glass. My mother carried the other. My little brother Sami carried the plastic bag, which held a football, and refused to let anyone help.\n\n"
                "The flat we were given was on the third floor, with a window that looked out over a car park and, beyond it, a single tree. My mother walked through every room twice. Then she opened the window, though it was February, and stood for a long moment looking at that tree. I did not understand, then, what she was doing. I think now that she was deciding to stay.\n\n"
                "People were kind to us, and I am grateful, but kindness can be difficult to receive. A woman from the flat below, Mrs Pritchard, brought us a box of tins and a pair of wellington boots for Sami, and spoke to us very loudly and slowly, as if we were hard of hearing rather than new to English. My father, who had taught mathematics to sixteen-year-olds for twenty years, thanked her in careful, perfect English, and I watched her face change.\n\n"
                "That was the first lesson I learned in Wales: that people would decide who we were before we had said a word, and that sometimes we would have to show them, gently, that they were wrong.\n\n"
                "School was harder. I understood more than I could say, which is a lonely place to be. For weeks I answered every question with a nod or a shrug, and I think my teacher, Mr Rees, believed I knew nothing. Then one wet afternoon he wrote a long division on the board and asked the class to solve it, and nobody moved, and I stood up, walked to the front and did it in silence, the way my father had taught me. Mr Rees looked at the board for a long time. “Well,” he said. “There's a lot I don't know about you, isn't there?”\n\n"
                "There was. There still is, about anyone.\n\n"
                "My grandmother's coat is still in the suitcase. She gave it to my mother on the morning we left, too heavy for the journey and too precious to leave behind. None of us has ever worn it. Every winter my mother takes it out, shakes it, and hangs it on the back of the bedroom door for one night, and then she folds it away again. When I asked her once why she did this, she said, “So it knows we are still here.”",
        "qs": [
            {"id": "f08354920a31", "t": "mcq", "d": "compare", "q": "How does the narrator contrast rain in Cardiff with rain in the city the family left?",
             "opts": ["There it was rare and welcomed; in Cardiff, constant and ordinary",
                      "There it was cold and unpleasant; in Cardiff it was warm and gentle",
                      "There it fell only in winter; in Cardiff it fell only in autumn",
                      "There it caused floods; in Cardiff it hardly fell at all"],
             "why": "In the old city, rain “was an event” and people turned their faces up to it; in Cardiff “rain was simply the air”: always there, unremarkable."},
            {"id": "f0364c558ac7", "t": "mcq", "d": "infer", "q": "What does the way the father packs his teaching certificates suggest?",
             "opts": ["They matter deeply to him, as proof of who he is and what he can do",
                      "They are the most valuable things to sell when the family arrives",
                      "He worries that the rain in Cardiff will make them go mouldy",
                      "He needs them to show the housing officer before he gets a flat"],
             "why": "He wraps them in a towel “as carefully as if they were made of glass”, beside the clothes and pots: they carry his twenty years of work and his hopes."},
            {"id": "20c7bdad2e53", "t": "mcq", "d": "structure", "q": "“I did not understand, then, what she was doing. I think now that she was deciding to stay.” What do these sentences show about how the account is told?",
             "opts": ["An adult is looking back and understands more than the child did",
                      "The narrator is reporting what the mother explained at the time",
                      "The story is told by the mother, years after the family arrived",
                      "The narrator is guessing about events that never really happened"],
             "no": {"The narrator is reporting what the mother explained at the time": "The mother explains nothing: “I did not understand, then”. The meaning is the narrator's own later reading."},
             "why": "The contrast between “then” and “now” shows a first-person narrator, grown up, reading the memory with understanding the ten-year-old did not have."},
            {"id": "caae2e016540", "t": "tap", "d": "retrieve", "q": "Tap the two words that show how Mrs Pritchard spoke to the family.",
             "s": "A woman from the flat below, Mrs Pritchard, brought us a box of tins and a pair of wellington boots for Sami, and spoke to us very [loudly] and [slowly], as if we were hard of hearing rather than new to English.",
             "why": "She spoke “very loudly and slowly”, as if they could not hear, which shows she had misjudged them."},
            {"id": "f525fb67043d", "t": "mcq", "d": "infer", "q": "Why does Mrs Pritchard's face change when the father thanks her?",
             "opts": ["She realises she had wrongly assumed they knew little",
                      "She is upset that he has refused the box of tins",
                      "She cannot understand his accent and feels embarrassed",
                      "She is annoyed that he did not speak more slowly"],
             "no": {"She cannot understand his accent and feels embarrassed": "He speaks in “careful, perfect English”, so she understands him well. What changes is her idea of who he is."},
             "why": "The next paragraph explains it: people “would decide who we were before we had said a word”. His perfect English shows her she was wrong."},
            {"id": "effa5051e016", "t": "mcq", "d": "language", "q": "The narrator says that understanding more than you can say “is a lonely place to be”. What is the effect of describing it as a place?",
             "opts": ["It makes the feeling seem like being shut away where nobody can reach you",
                      "It shows that the school building was far away from the family's flat",
                      "It suggests the narrator liked to spend time alone in a quiet room",
                      "It tells the reader that the narrator often got lost in the new school"],
             "why": "The metaphor makes a feeling into somewhere you are trapped: the narrator can follow everything but cannot reach others with words."},
            {"id": "a1cef4727fd4", "t": "mcq", "d": "infer", "q": "What does the mother's yearly habit with the grandmother's coat suggest?",
             "opts": ["She keeps a living link to the family and the home they left",
                      "She is planning to sell the coat when the family needs money",
                      "She wants to wear the coat but finds Cardiff too wet for it",
                      "She has forgotten the coat until she finds it each winter"],
             "why": "The coat was “too precious to leave behind” and is never worn, only aired. “So it knows we are still here” shows it stands for the grandmother and the past they carry with them."},
        ],
    },
    # ------------------------------------------------------------------ RD8.11
    {
        "key": "RD8.11",
        "year": 8,
        "strand": "Letters and diaries",
        "title": "A Letter of Complaint",
        "nc": "Understand increasingly challenging texts: know the purpose, audience for and context of the writing",
        "text": "14 Linden Grove\nHarrogate\nHG2 7PL\n\n"
                "12 March\n\n"
                "Mr D. Haldane\nCustomer Services Manager\nWestvale Coaches\nUnit 4, Riverside Park\nLeeds\nLS10 3QT\n\n"
                "Dear Mr Haldane,\n\n"
                "Booking reference WV-2291: coach for the Ashfield Academy Youth Orchestra, Saturday 2 March\n\n"
                "I am writing as chair of the Ashfield Academy Youth Orchestra parents' committee to complain about your company's failure to provide the coach we booked, and about the way our enquiries were handled afterwards.\n\n"
                "Six weeks in advance, the committee booked a 53-seat coach to take forty-one pupils and their instruments to the Northern Schools Music Festival in York. The booking was confirmed in writing, and we paid the full fee of £640 on 20 January. The coach was due at the school at 7.30 a.m.\n\n"
                "It did not arrive. Between 7.30 and 8.15 a.m. I telephoned your office six times. On four occasions nobody answered; on the other two I was told that “someone is looking into it”. At 8.20 a.m. parents began driving pupils to York in their own cars. Because cellos and double basses do not fit easily into family cars, three pupils were unable to travel at all. The orchestra performed with an incomplete string section and lost the chance to compete for a place in the regional final.\n\n"
                "I appreciate that vehicles break down and that drivers fall ill. I do not expect any company to be free of problems. What I do expect is to be told about them. A single telephone call at 7 a.m. would have given us time to make other arrangements. Instead, forty-one young people stood in the rain outside their school for nearly an hour, holding instruments they had practised on for months.\n\n"
                "Since the festival, I have written to your company twice, on 4 March and 7 March. I have received one automated email and no reply.\n\n"
                "I am therefore asking for:\n1. a full refund of £640;\n2. a written explanation of why the coach did not arrive and why we were not informed;\n3. an assurance of the steps you will take to prevent this happening to other customers.\n\n"
                "I would be grateful for a reply within fourteen days of the date of this letter. If I do not receive one, I shall seek further advice about our rights as customers.\n\n"
                "Yours sincerely,\n\n"
                "Folasade Adeyemi (Mrs)\nChair, Ashfield Academy Youth Orchestra Parents' Committee",
        "qs": [
            {"id": "f06660b5c366", "t": "mcq", "d": "structure", "q": "Why does the writer put the booking reference on its own line just after “Dear Mr Haldane”?",
             "opts": ["So the reader sees at once which booking the letter is about",
                      "So the company knows how much money she paid for the coach",
                      "So that the letter will be passed on to the coach driver",
                      "So the orchestra's name appears above her own signature"],
             "why": "A subject line in a formal letter tells the reader straight away what it concerns; the reference lets the company find the booking quickly."},
            {"id": "3650f2d7c54c", "t": "text", "d": "retrieve", "q": "How many times did the writer telephone the coach company's office before 8.15 a.m.? Type the number.",
             "a": ["six", "6", "six times"],
             "why": "The third paragraph says: “Between 7.30 and 8.15 a.m. I telephoned your office six times.”"},
            {"id": "f5559e09c21c", "t": "mcq", "d": "retrieve", "q": "According to the letter, why were three pupils unable to travel to York?",
             "opts": ["Their large instruments would not fit in family cars", "Their parents could not leave work that morning",
                      "They had gone home when the coach did not come", "They were not well enough to play at the festival"],
             "why": "The letter says: “Because cellos and double basses do not fit easily into family cars, three pupils were unable to travel at all.”"},
            {"id": "8523bb0e5821", "t": "mcq", "d": "structure", "q": "The fourth paragraph begins: “I appreciate that vehicles break down and that drivers fall ill.” Why does the writer include this?",
             "opts": ["To sound fair, and show her real complaint is about not being told",
                      "To excuse the company, because she has decided not to ask for a refund",
                      "To explain that the coach broke down on the motorway near York",
                      "To show that she is unsure whether the company is to blame"],
             "no": {"To explain that the coach broke down on the motorway near York": "The letter never says why the coach failed to come; asking for “a written explanation” shows she does not know."},
             "why": "By admitting problems happen, she sounds fair, then narrows her point: “What I do expect is to be told about them.”"},
            {"id": "19c6dc8a6487", "t": "mcq", "d": "language", "q": "What is the main effect of the sentence about forty-one young people standing in the rain “holding instruments they had practised on for months”?",
             "opts": ["It makes the reader feel the human cost of the company's silence",
                      "It proves that the instruments were damaged by the wet weather",
                      "It shows that the pupils were not ready for the festival",
                      "It gives the exact time that the coach should have arrived"],
             "why": "The writer moves from facts to a picture of disappointed pupils, so the manager feels what the failure to phone meant to real people."},
            {"id": "e9d8aef5c50d", "t": "mcq", "d": "vocab", "q": "She asks for “an assurance of the steps you will take”. What does assurance mean here?",
             "opts": ["a firm promise", "a cash payment", "a polite apology", "a written warning"],
             "no": {"a polite apology": "An apology says sorry for the past; an assurance is a promise about the future, here about the steps the company will take."},
             "why": "An assurance is a confident promise that something will happen: she wants the company to commit to preventing a repeat."},
            {"id": "b1dd7734692f", "t": "mcq", "d": "purpose", "q": "Which best describes the tone of the whole letter?",
             "opts": ["Firm and serious, but calm and polite throughout",
                      "Angry and insulting, with many exclamation marks",
                      "Friendly and chatty, as if writing to a neighbour",
                      "Nervous and apologetic, as if she is to blame"],
             "why": "She states facts, dates and clear demands and sets a deadline, but never insults the reader: “I would be grateful for a reply” keeps it polite."},
        ],
    },
    # ------------------------------------------------------------------ RD8.12
    {
        "key": "RD8.12",
        "year": 8,
        "strand": "Information",
        "title": "Into the Deep Ocean",
        "nc": "Understand increasingly challenging texts: learn new vocabulary and make inferences, referring to evidence in the text",
        "text": "The ocean covers about seven-tenths of the Earth's surface, and on average it is several kilometres deep. Yet the deep ocean remains one of the least explored places on our planet: the surface of the Moon has been mapped in more detail than much of our own sea floor.\n\n"
                "Light is the first thing to disappear. Seawater absorbs sunlight quickly, so by about 200 metres below the surface there is too little for plants and algae to grow. Below about 1,000 metres there is no sunlight at all. Scientists often divide the ocean into zones to describe this change: a sunlit zone near the surface, a dim twilight zone beneath it, and then a vast midnight zone stretching down towards the sea floor.\n\n"
                "The second challenge is pressure. At the surface, the weight of the air above us presses on every part of our bodies. Every ten metres of seawater adds roughly the same pressure again. At the bottom of the deepest place known, the Challenger Deep in the Mariana Trench in the Pacific Ocean, nearly 11 kilometres down, the pressure is more than a thousand times that at the surface. The first people to reach it, in 1960, travelled inside a thick-walled steel sphere.\n\n"
                "Life, astonishingly, has found ways to cope. Many deep-sea animals have soft, watery bodies with no air spaces that could be crushed. Because food is scarce, many move slowly and can survive long periods between meals. Much of what they eat drifts down from above: a steady fall of dead plankton and other scraps, which scientists call marine snow.\n\n"
                "In the darkness, many creatures make their own light, a process called bioluminescence. Some use flashes of light to confuse attackers, some to signal to one another, and the anglerfish dangles a glowing lure in front of its mouth to attract prey.\n\n"
                "The greatest surprise came in 1977. Scientists exploring the sea floor near the Galápagos Islands found hydrothermal vents: cracks where water heated by hot rock beneath the sea floor gushes out, rich in dissolved chemicals. Around them lived crowded communities of giant tube worms, clams and crabs. These animals did not depend on sunlight at all. Instead, bacteria were using the chemicals from the vents to make food, a process called chemosynthesis, and other animals fed on the bacteria or lived alongside them.\n\n"
                "This discovery changed what scientists believed life needs. Before 1977, it was generally assumed that almost all life on Earth depended, in the end, on the Sun. Now we know that whole communities can be powered by the chemistry of the Earth itself. Some scientists even think that places like these are where we should search for life beyond our planet, in the hidden oceans thought to lie beneath the ice of certain moons.\n\n"
                "Every deep-sea expedition still finds species no one has seen before. The deep ocean is not an empty darkness. It is a world we have barely begun to visit.",
        "qs": [
            {"id": "7961440a25c1", "t": "text", "d": "retrieve", "q": "According to the text, by about how many metres below the surface is there too little light for plants and algae to grow? Type the number.",
             "a": ["200", "about 200", "200 metres", "200 m", "two hundred"],
             "why": "The second paragraph says “by about 200 metres below the surface there is too little for plants and algae to grow”. All light is gone below about 1,000 metres."},
            {"id": "9e57f6e84d75", "t": "order", "d": "sequence", "q": "Put these in order from the surface of the ocean downwards, as the text describes them.",
             "items": ["the sunlit zone", "the twilight zone", "the midnight zone", "the sea floor"],
             "why": "The text lists “a sunlit zone near the surface, a dim twilight zone beneath it, and then a vast midnight zone stretching down towards the sea floor”."},
            {"id": "ceb85ad24c8a", "t": "mcq", "d": "vocab", "q": "“Because food is scarce, many move slowly.” What does scarce mean here?",
             "opts": ["in short supply", "hard to digest", "found only at night", "dangerous to catch"],
             "why": "Scarce means there is not much of it. Food is hard to come by, so animals save energy by moving slowly."},
            {"id": "9388345c763c", "t": "tap", "d": "retrieve", "q": "Tap the two words of the name scientists give to the scraps that drift down from above.",
             "s": "Much of what they eat drifts down from above: a steady fall of dead plankton and other scraps, which scientists call [marine] [snow].",
             "why": "Scientists call it marine snow: dead plankton and other scraps falling slowly, like snow, from the waters above."},
            {"id": "083a7b132c18", "t": "mcq", "d": "compare", "q": "How did the 1977 discovery change what scientists believed about life?",
             "opts": ["They had thought almost all life relied on the Sun; now they knew some relied on chemicals",
                      "They had thought nothing lived in the deep; now they knew bacteria lived only at the surface",
                      "They had thought life needed chemicals; now they knew it needed only sunlight",
                      "They had thought vents were common; now they knew they were found only near the Galápagos"],
             "no": {"They had thought life needed chemicals; now they knew it needed only sunlight": "This reverses it: the vent animals “did not depend on sunlight at all”."},
             "why": "The seventh paragraph says that before 1977 almost all life was assumed to depend on the Sun; now we know whole communities can be powered “by the chemistry of the Earth itself”."},
            {"id": "b54dbbe8fb8c", "t": "mcq", "d": "structure", "q": "The text ends: “The deep ocean is not an empty darkness. It is a world we have barely begun to visit.” What is the effect of this ending?",
             "opts": ["It corrects a common idea of the deep and stresses how much is unknown",
                      "It warns readers that visiting the deep ocean is too dangerous to attempt",
                      "It sums up the dangers of pressure that were explained in the third paragraph",
                      "It suggests that scientists have now explored most of the deep sea floor"],
             "no": {"It suggests that scientists have now explored most of the deep sea floor": "“Barely begun” means the opposite: very little has been explored, which links back to the opening."},
             "why": "Setting “not an empty darkness” against “a world” replaces a gloomy picture with a living one, and “barely begun” echoes the opening point that the deep is hardly explored."},
            {"id": "c444d04ccac2", "t": "mcq", "d": "purpose", "q": "What is the main purpose of the text?",
             "opts": ["To inform readers about conditions and life in the deep ocean",
                      "To persuade readers to train as deep-sea scientists",
                      "To tell the story of the first journey to the Challenger Deep",
                      "To explain how bioluminescence works in the anglerfish"],
             "why": "It explains light, pressure, food, bioluminescence and the vents: the dive of 1960 and the anglerfish are single examples within that wider aim."},
        ],
    },
]
