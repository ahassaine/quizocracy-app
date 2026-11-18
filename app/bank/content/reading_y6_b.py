"""Reading comprehension, Year 6, second set (keys RD6.17-RD6.32): 16 passages of 300-450 words, 7-8 questions each.

Spec: app/bank/SPEC_READING.md (and SPEC.md for the question format). Every passage and question is
original writing, written by hand, to prepare for the KS2 SATs reading paper, on different topics from
reading_y6.py: questions are phrased the way the paper asks them ("Find and copy...", "Which word is closest
in meaning to...", "Why did the writer...", "Using information from the text...", "Which of these is an
opinion?").

Topics: lightning, Britain's canals, how glass is made (information); how a hot-air balloon flies
(explanation); a biography of Florence Nightingale; a diary of the 1969 Moon landing; building a bug hotel
(instructions); planting street trees (persuasive); a news report on a library saved by volunteers; a
play script set in a railway station; two poems (a city before dawn, a great-grandfather's toolbox); and
stories set on the Anglesey coast, in a Mumbai monsoon, in a classroom bridge-building challenge, plus a
fable (the magpie and the mole). Evolution, puberty and human reproduction are left out, as promised to
families.

The questions cover every KS2 reading domain (retrieve, infer, vocab, sequence, summarise, structure,
language, compare, predict, purpose), retrieval and inference most often. To be checked line by line by a
second reviewer (facts, one defensible answer per question, no leaks) before scripts/bank_ids.py gives the
questions their ids.
"""

SKILLS = [
    {
        "key": "RD6.17",
        "year": 6,
        "strand": "Stories",
        "title": "The tide clock",
        "nc": "Draw inferences such as inferring characters' feelings, thoughts and motives from their actions",
        "text": (
            "Ffion had lived beside the Menai Strait all her life, so she knew the rule by heart: always check the "
            "tide before crossing to the island. The island was really a rocky hump of grass called Ynys Fach, and "
            "at low tide a ridge of sand and shingle joined it to the beach. At high tide, the ridge vanished under "
            "fast, grey water.\n\n"
            "On Saturday afternoon, her little brother Gethin begged to go and look at the seals that sometimes lay "
            "on the far rocks. Ffion glanced at the tide clock in the kitchen. Its single hand pointed just past "
            "low water.\n\n"
            "“We've got an hour,” she said. “Not a minute more.”\n\n"
            "They crunched across the ridge, and on the far side two seals were stretched out on a ledge, as round "
            "and lazy as sacks of flour. Gethin lay on his stomach to watch them. Ffion lay beside him. The seals "
            "yawned, rolled and scratched themselves with their flippers, and the hour slipped away as quietly as "
            "the water was creeping in.\n\n"
            "When Ffion finally looked back towards the beach, her heart lurched. The ridge had shrunk to a thin "
            "brown ribbon, and the sea was already licking at both sides of it.\n\n"
            "“Run?” said Gethin.\n\n"
            "Ffion thought of the stories her grandad told about people swept off their feet by the current, and "
            "she shook her head. “We stay,” she said firmly. “The island's high. The water can't reach the top.”\n\n"
            "She phoned home. Her voice wobbled only once. Mum told her to stay where she was, to keep warm and "
            "not to move, and said she would call the coastguard straight away.\n\n"
            "They climbed to the highest point and sat back to back in the wind. Ffion counted the waves to stop "
            "herself thinking. Gethin counted the seals, who had slid into the water and were now bobbing about, "
            "watching the two children as if they were the strange ones.\n\n"
            "Forty minutes later, a small orange lifeboat came round the point. The crew member who helped them "
            "aboard was smiling.\n\n"
            "“You did exactly the right thing,” she said. “Most people try to run back. Staying put is what keeps "
            "you safe.”\n\n"
            "That evening, Ffion took a marker pen and drew a thick red line on the tide clock, an hour after low "
            "water. Underneath, she wrote: TIME TO GO."
        ),
        "qs": [
            {"id": "701424c01185", "t": "text", "d": "retrieve", "q": "What joined Ynys Fach to the beach at low tide? Find and copy one word.",
             "a": ["ridge", "a ridge", "the ridge", "ridges"],
             "why": "The first paragraph says that at low tide a ridge of sand and shingle joined it to the beach."},
            {"id": "cc2576f1a953", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you how the water moves at high tide.",
             "s": "At high tide, the ridge vanished under [fast], grey water.",
             "why": "The water at high tide is fast: that is why crossing then is dangerous."},
            {"id": "aa7bdc73cba1", "t": "mcq", "d": "vocab", "q": "“When Ffion finally looked back towards the beach, her heart lurched.” Which is closest in meaning to “her heart lurched”?",
             "opts": ["her heart gave a sudden jump of fear", "her heart slowed down and calmed",
                      "her heart ached because she was sad", "her heart beat in time with the waves"],
             "why": "To lurch is to make a sudden, jerking movement: she has just seen the ridge disappearing, so it is a jolt of fear."},
            {"id": "c3ab9d1b673d", "t": "mcq", "d": "infer", "q": "Why did Ffion decide not to run back across the ridge?",
             "opts": ["She feared the current could knock them off their feet.",
                      "She wanted to stay and watch the seals for longer.",
                      "Mum had told her on the phone to stay on the island.",
                      "Gethin was too tired to run all the way back."],
             "why": "She thought of her grandad's stories about people swept off their feet by the current. Mum's advice came later, after she had already decided."},
            {"id": "fd8dc3ae468c", "t": "mcq", "d": "infer", "q": "“Her voice wobbled only once.” What does this suggest about Ffion on the phone?",
             "opts": ["She was frightened but working hard to stay calm.",
                      "She was shivering because the wind was so cold.",
                      "She could hardly hear Mum over the waves.",
                      "She was cross with Gethin for wanting to come."],
             "why": "A wobbling voice shows fear; that it wobbled only once shows she kept control of it for her brother's sake."},
            {"id": "91ffe2ab10b1", "t": "order", "d": "sequence", "q": "Put these events in the order they happen in the story.",
             "items": ["Ffion checked the tide clock in the kitchen.",
                       "The children watched the seals on a ledge.",
                       "Ffion phoned home.",
                       "A lifeboat came round the point.",
                       "Ffion drew a red line on the tide clock."],
             "why": "She checked the clock before leaving, lost track of time watching the seals, phoned once they were cut off, was rescued, and marked the clock that evening."},
            {"id": "692a548d0b89", "t": "mcq", "d": "summarise", "q": "Why did Ffion draw the red line and write TIME TO GO?",
             "opts": ["She had learned to keep track of time and leave the island early.",
                      "She wanted to remember the day she first saw the seals.",
                      "The lifeboat crew had asked her to mark the tide clock.",
                      "She planned to cross to the island at high tide next time."],
             "why": "The hour had slipped away while they watched the seals; the line marks when she must start back so it never happens again."},
        ],
    },
    {
        "key": "RD6.18",
        "year": 6,
        "strand": "Information",
        "title": "Lightning: a spark in the sky",
        "nc": "Retrieve, record and present information from non-fiction; explain and discuss understanding of what has been read",
        "text": (
            "A summer storm can turn a hot, heavy afternoon into a spectacle of light and noise. Lightning is one "
            "of the most powerful things in nature, and it flashes millions of times every day somewhere on Earth. "
            "Yet it begins with something as small as a speck of ice.\n\n"
            "Inside a tall storm cloud, strong currents of air carry drops of water high up, to where it is "
            "freezing. There, tiny crystals of ice and soft pellets of ice crash into each other again and again. "
            "Each bump moves a little electric charge from one piece of ice to another, rather like the static "
            "that builds up when you rub a balloon on a jumper. Slowly, one part of the cloud gathers one kind of "
            "charge and another part gathers the opposite kind.\n\n"
            "When the difference becomes too great, the charge leaps across the gap in a giant spark. That spark "
            "is lightning. Some flashes stay inside the cloud, but others strike the ground, often hitting the "
            "highest point nearby, such as a tree, a tower or a hilltop.\n\n"
            "A flash of lightning lasts less than a second, but it heats the air around it until it is hotter "
            "than the surface of the Sun. The air expands so suddenly that it makes a huge boom, which we hear as "
            "thunder. The flash and the boom happen at the same moment, but light travels much faster than sound, "
            "so we see the lightning before we hear the rumble.\n\n"
            "This gives you a simple way to tell how far away a storm is. When you see a flash, count the seconds "
            "until you hear the thunder. Every three seconds is roughly one kilometre. If the gap gets shorter "
            "each time, the storm is coming towards you.\n\n"
            "Lightning can be dangerous, so it is worth knowing how to stay safe. The best place to be is "
            "indoors, away from windows. A car with a metal roof is safe too, as long as the windows are shut. "
            "Outdoors, never shelter under a lone tree, and keep away from water and open hilltops. If you can "
            "hear thunder, you are close enough to be struck.\n\n"
            "Tall buildings are protected by lightning conductors: metal strips that run from the roof down into "
            "the ground. If lightning strikes, the electricity travels safely down the strip instead of through "
            "the building. So the next time a storm rolls in, you can enjoy the show and understand exactly what "
            "is happening, as long as you watch from somewhere safe."
        ),
        "qs": [
            {"id": "bc395d01f4fe", "t": "mcq", "d": "vocab", "q": "“A summer storm can turn a hot, heavy afternoon into a spectacle of light and noise.” Which word or phrase is closest in meaning to spectacle?",
             "opts": ["an amazing sight", "a loud warning", "a sudden change", "a heavy shower"],
             "why": "A spectacle is something striking to watch: the flashes and booms of a storm make an impressive show, as the last paragraph also says."},
            {"id": "c11fdada069d", "t": "mcq", "d": "retrieve", "q": "According to the second paragraph, what carries drops of water up to where it is freezing?",
             "opts": ["strong currents of air", "electric charges", "tiny crystals of ice", "soft pellets of ice"],
             "why": "The second paragraph says strong currents of air carry drops of water high up, to where it is freezing. The ice forms after that."},
            {"id": "1aae64f86fc9", "t": "mcq", "d": "language", "q": "Why does the writer mention rubbing a balloon on a jumper?",
             "opts": ["to compare the charge in a cloud with something readers may have tried",
                      "to show that storms begin when balloons are rubbed together",
                      "to explain why storm clouds look soft and woolly",
                      "to warn readers not to play with balloons in a storm"],
             "why": "Static from a rubbed balloon is a familiar example of charge building up, so it helps readers picture what happens to the ice in the cloud."},
            {"id": "2d1b87d575dc", "t": "tap", "d": "retrieve", "q": "Tap the word that tells you how quickly the air expands.",
             "s": "The air expands so [suddenly] that it makes a huge boom, which we hear as thunder.",
             "why": "The fourth paragraph says the air expands so suddenly that it makes a boom."},
            {"id": "c471e6312f5e", "t": "mcq", "d": "infer", "q": "Aisha sees a flash and counts nine seconds before she hears the thunder. Using the text, about how far away is the storm?",
             "opts": ["about three kilometres", "about nine kilometres", "about one kilometre", "about twenty-seven kilometres"],
             "why": "The text says every three seconds is roughly one kilometre, and nine seconds is three lots of three seconds."},
            {"id": "1d2ce32bb008", "t": "mcq", "d": "retrieve", "q": "According to the text, when is a car a safe place to be in a thunderstorm?",
             "opts": ["when it has a metal roof and the windows are shut",
                      "when it is parked under a tall tree",
                      "when it is driving away from the storm",
                      "when its engine has been switched off"],
             "why": "The sixth paragraph says a car with a metal roof is safe, as long as the windows are shut. Sheltering under a tree is what it warns against."},
            {"id": "96fe38d63395", "t": "mcq", "d": "purpose", "q": "What is the main purpose of this text?",
             "opts": ["to explain how lightning happens and how to stay safe",
                      "to persuade readers to stay indoors all summer",
                      "to tell the story of a storm one family watched",
                      "to describe how a lightning conductor is fitted"],
             "why": "The text explains how lightning and thunder form, how to tell how far off a storm is, and how to keep safe."},
        ],
    },
    {
        "key": "RD6.19",
        "year": 6,
        "strand": "Letters and diaries",
        "title": "The night of the Moon landing",
        "nc": "Draw inferences such as inferring characters' feelings, thoughts and motives from their actions; justify inferences with evidence",
        "text": (
            "Sunday 20th July 1969\n\n"
            "Tonight two men are going to land on the Moon, and Dad says I can stay up to watch, even though it is "
            "school tomorrow. Mum said no at first. Then Dad said, “Gloria, this will only happen once in his whole "
            "life,” and she gave in, although she made me have a bath first.\n\n"
            "The spacecraft is called Apollo 11. It took off from America four days ago, and there are three "
            "astronauts: Neil Armstrong, Buzz Aldrin and Michael Collins. Collins has to stay in the main ship, "
            "going round and round the Moon, while the other two go down in a little lander called the Eagle. I "
            "think that would be the worst job in the world. Imagine getting all that way and not even setting "
            "foot on it.\n\n"
            "At a little after nine o'clock we heard a crackly voice say, “The Eagle has landed.” Grandma, who had "
            "come round specially, clapped her hands and said, “Well, I never!” But they are not getting out yet. "
            "The man on the television says it will be hours.\n\n"
            "Monday 21st July 1969\n\n"
            "I did it! I stayed up the whole night, although I think I fell asleep for a bit on the settee. Dad "
            "woke me at nearly four o'clock in the morning. The picture on our television was grey and fuzzy, like "
            "looking through a dirty window, but you could see a pale shape climbing slowly down a ladder.\n\n"
            "Then Neil Armstrong said, “That's one small step for man, one giant leap for mankind.” Dad didn't say "
            "anything. He just squeezed my shoulder, very hard.\n\n"
            "At school everybody was yawning. Mrs Hughes asked who had watched, and nearly every hand went up. "
            "She let us draw the Moon instead of doing spellings.\n\n"
            "Thursday 24th July 1969\n\n"
            "They are home! The capsule splashed down in the Pacific Ocean today, and all three astronauts are "
            "safe. I have started a scrapbook of newspaper cuttings, and on the very first page I have stuck a "
            "picture of Michael Collins, because somebody has to remember him too.\n\n"
            "When I grow up, I am going to be an engineer and build rockets. Mum says I had better start by "
            "building a tidier bedroom.\n\n"
            "Delroy"
        ),
        "qs": [
            {"id": "7c56f084151f", "t": "mcq", "d": "retrieve", "q": "What did Mum make Delroy do before he could stay up?",
             "opts": ["have a bath", "tidy his bedroom", "finish his spellings", "go to bed early"],
             "why": "The first entry says she gave in, although she made him have a bath first. The tidy bedroom comes in the last entry."},
            {"id": "526872c0073a", "t": "mcq", "d": "compare", "q": "How was Michael Collins's job different from the jobs of the other two astronauts?",
             "opts": ["He stayed in the main ship circling the Moon while they went down to it.",
                      "He walked on the Moon first while they waited in the main ship.",
                      "He steered the Eagle down while they stayed behind in America.",
                      "He spoke to the people on Earth while they slept in the lander."],
             "why": "The first entry says Collins stayed in the main ship going round the Moon while Armstrong and Aldrin went down in the Eagle."},
            {"id": "76ab1a285a56", "t": "text", "d": "retrieve", "q": "What was the name of the little lander? Find and copy.",
             "a": ["the Eagle", "Eagle", "an Eagle"],
             "why": "Delroy writes that the other two went down in a little lander called the Eagle."},
            {"id": "5ee301426763", "t": "mcq", "d": "language", "q": "Delroy says the picture was “like looking through a dirty window”. What does this tell you about the picture?",
             "opts": ["It was blurred and hard to see clearly.", "It was bright and full of colour.",
                      "It kept switching off and on again.", "It showed the Moon through a window."],
             "why": "Through a dirty window things look smudged and unclear: the picture was grey and fuzzy."},
            {"id": "33338c2e88e1", "t": "mcq", "d": "infer", "q": "“Dad didn't say anything. He just squeezed my shoulder, very hard.” What does this suggest about Dad?",
             "opts": ["He was too moved by the moment to speak.",
                      "He was cross that Delroy had fallen asleep.",
                      "He was worried about Delroy being tired at school.",
                      "He could not hear the words on the television."],
             "why": "He had persuaded Mum it was a once-in-a-lifetime event; staying silent and gripping his son's shoulder shows strong feeling."},
            {"id": "dedc4ac13ed3", "t": "order", "d": "sequence", "q": "Put these events in the order they happened.",
             "items": ["A voice said that the Eagle had landed.",
                       "Dad woke Delroy at nearly four o'clock.",
                       "Neil Armstrong spoke his famous words.",
                       "Mrs Hughes let the class draw the Moon.",
                       "The capsule splashed down in the Pacific."],
             "why": "The landing was on Sunday evening; Dad woke him for the first step early on Monday; school came later that day; the splashdown was on Thursday."},
            {"id": "d53cd5a9880d", "t": "mcq", "d": "infer", "q": "Why did Delroy put a picture of Michael Collins on the first page of his scrapbook?",
             "opts": ["He felt Collins should be remembered, even without walking on the Moon.",
                      "Collins was the first of the three astronauts to step onto the Moon.",
                      "It was the only picture of an astronaut in any of the newspapers.",
                      "Mrs Hughes had asked everyone in the class to write about Collins."],
             "why": "Delroy thought Collins had the worst job, coming all that way without setting foot on the Moon, and writes that “somebody has to remember him too”."},
        ],
    },
    {
        "key": "RD6.20",
        "year": 6,
        "strand": "Biography",
        "title": "Florence Nightingale",
        "nc": "Retrieve, record and present information; summarise the main ideas drawn from more than one paragraph",
        "text": (
            "Florence Nightingale was born in 1820 in the Italian city of Florence, while her wealthy British "
            "parents were travelling there, and she was named after it. She grew up in England, in large country "
            "houses, and her father taught her history, languages and mathematics.\n\n"
            "As a young woman, Florence was expected to marry, run a household and spend her time on visits and "
            "parties. But she wanted something different: she wanted to be a nurse. Her family was horrified. At "
            "that time, nursing was not seen as a respectable job for a woman from a family like hers, and "
            "hospitals were often dirty, crowded places. For years Florence argued with her parents, and she read "
            "everything she could find about hospitals. At last, in her thirties, she trained as a nurse in "
            "Germany, and then she ran a small hospital in London.\n\n"
            "In 1854, Britain was fighting in the Crimean War. Newspapers reported terrible conditions in the army "
            "hospital at Scutari, in what is now Turkey, where sick and wounded soldiers lay on filthy floors "
            "without enough clean water, blankets or proper food. The government asked Florence to help, and she "
            "sailed out with a team of thirty-eight nurses.\n\n"
            "What she found was shocking. Far more soldiers were dying from diseases such as cholera and typhus "
            "than from their wounds. Florence and her nurses scrubbed the wards, washed the bedding and organised "
            "better food. A team sent from Britain cleared out the drains and improved the water supply, and soon "
            "far fewer patients were dying. At night, Florence walked the long wards carrying a lamp to check on "
            "the patients, and the soldiers called her “the Lady with the Lamp”.\n\n"
            "When she returned home, Florence was famous, but she did not rest. She collected careful figures "
            "about how many soldiers had died and why. Then she turned them into colourful diagrams that showed at "
            "a glance that most of the deaths could have been prevented by better hygiene. These diagrams helped "
            "to persuade the government to improve army hospitals.\n\n"
            "In 1860, she opened a school for training nurses at St Thomas' Hospital in London. Nurses who trained "
            "there went on to work all over the world, and nursing slowly became a respected career. Florence "
            "Nightingale died in 1910, at the age of ninety. Today, International Nurses Day is held every year on "
            "12th May, her birthday."
        ),
        "qs": [
            {"id": "8d337809bac6", "t": "mcq", "d": "retrieve", "q": "According to the text, why was Florence given her name?",
             "opts": ["She was born in the city of Florence.", "It was the name of her father's mother.",
                      "Her parents chose it from a history book.", "It was the name of a famous nurse."],
             "why": "The first paragraph says she was born in Florence while her parents were travelling, and was named after the city."},
            {"id": "8c571ab029e9", "t": "mcq", "d": "infer", "q": "Why do you think Florence's family was “horrified” when she said she wanted to be a nurse?",
             "opts": ["They thought nursing was not a proper job for a woman like her.",
                      "They thought she was not clever enough to train as a nurse.",
                      "They wanted her to become a teacher of mathematics.",
                      "They did not want her to travel to the Crimean War."],
             "why": "The second paragraph says nursing was not seen as respectable for a woman from a family like hers; she was expected to marry and run a household. The war came years later."},
            {"id": "37212b23e6aa", "t": "mcq", "d": "vocab", "q": "“Nursing was not seen as a respectable job.” Which word is closest in meaning to respectable?",
             "opts": ["proper", "difficult", "tiring", "exciting"],
             "why": "Something respectable is thought proper and decent by other people: her family did not think nursing was a suitable job."},
            {"id": "7a7476618caf", "t": "text", "d": "retrieve", "q": "How many nurses sailed out to Scutari with Florence? Write the number.",
             "a": ["38", "thirty-eight", "thirty eight", "38 nurses", "thirty-eight nurses"],
             "why": "The third paragraph says she sailed out with a team of thirty-eight nurses."},
            {"id": "1b41a8810fa1", "t": "mcq", "d": "infer", "q": "Why did Florence turn her figures into diagrams, rather than just giving lists of numbers?",
             "opts": ["Diagrams showed her main point quickly to the people she had to persuade.",
                      "The government had asked her to draw pictures of the hospital at Scutari.",
                      "She had lost some of her figures and could not write them out in full.",
                      "Diagrams were the only way to record how many nurses she had trained."],
             "why": "The fifth paragraph says the diagrams “showed at a glance” that most deaths could have been prevented, and that they helped to persuade the government."},
            {"id": "656da1d57ca9", "t": "order", "d": "sequence", "q": "Put these events in the order they happened in Florence's life.",
             "items": ["Florence trained as a nurse in Germany.",
                       "She sailed to Scutari with a team of nurses.",
                       "She made diagrams of how the soldiers had died.",
                       "She opened a school for nurses in London."],
             "why": "She trained in her thirties, went to Scutari in 1854, made her diagrams after she came home, and opened the school in 1860."},
            {"id": "61b65a816202", "t": "mcq", "d": "summarise", "q": "Which statement best sums up why Florence Nightingale is remembered?",
             "opts": ["She made hospitals cleaner and nursing more respected.",
                      "She was the first woman to study mathematics.",
                      "She built the army hospital at Scutari.",
                      "She invented the medicine that cured cholera."],
             "why": "The text shows her cleaning up the wards, using figures to get army hospitals improved, and training nurses so nursing became a respected career."},
        ],
    },
    {
        "key": "RD6.21",
        "year": 6,
        "strand": "Explanations",
        "title": "How a hot-air balloon flies",
        "nc": "Retrieve and record information from non-fiction; identify how structure and presentation contribute to meaning",
        "text": (
            "Hot-air balloons look as if they float without any effort, drifting silently over fields and towns. "
            "In fact, they rely on one simple scientific idea: hot air rises.\n\n"
            "When air is heated, its tiny particles move faster and spread further apart. This means that a "
            "balloon full of hot air is lighter than the same amount of space filled with the cooler air around "
            "it. Just as a cork bobs up through water to the surface, the hot air is pushed upwards through the "
            "cooler air, and it carries the balloon with it.\n\n"
            "A hot-air balloon has three main parts. The envelope is the huge, colourful bag that holds the hot "
            "air. It is made of a strong, light fabric such as nylon. Below the envelope hangs the basket, usually "
            "woven from wicker, which carries the pilot and passengers. Wicker is used because it is light and "
            "slightly springy, so it bends rather than breaks on a bumpy landing. Between them is the burner, which "
            "burns gas from tanks stored in the basket and sends a roaring flame up into the envelope.\n\n"
            "To go up, the pilot fires the burner, and the air inside the envelope gets hotter. To come down, the "
            "pilot simply waits: the air slowly cools, and the balloon sinks. For a quicker descent, the pilot can "
            "pull a cord that opens a vent at the top of the envelope and lets some of the hot air escape.\n\n"
            "There is one thing a balloon pilot cannot do, and that is steer. A balloon travels wherever the wind "
            "blows it. However, the wind often blows in different directions at different heights, so a skilled "
            "pilot can rise or sink to find a wind that is heading the right way. Most flights take place soon "
            "after sunrise or shortly before sunset, when the winds are usually gentle.\n\n"
            "The first hot-air balloon to carry passengers was built in France in 1783 by two brothers, Joseph and "
            "Étienne Montgolfier. Its passengers were a sheep, a duck and a cockerel, and all three landed safely. "
            "About two months later, two men became the first people to fly freely in a balloon. More than two "
            "hundred years on, balloons still use the same simple idea that lifted that surprised sheep into the "
            "sky."
        ),
        "qs": [
            {"id": "3843a428f263", "t": "text", "d": "retrieve", "q": "What simple scientific idea do hot-air balloons rely on? Find and copy three words.",
             "a": ["hot air rises"],
             "why": "The first paragraph says balloons rely on one simple scientific idea: hot air rises."},
            {"id": "4bf5bb5a5453", "t": "mcq", "d": "language", "q": "Why does the writer mention a cork bobbing up through water?",
             "opts": ["to help readers picture how something lighter is pushed upwards",
                      "to show that balloons are made from cork and float on lakes",
                      "to explain why balloons must never land on water",
                      "to describe the shape of the envelope when it is full"],
             "why": "A cork is lighter than water and is pushed up to the surface; in the same way hot air is pushed up through cooler air."},
            {"id": "8283ae62e02e", "t": "mcq", "d": "retrieve", "q": "According to the text, why is the basket usually made of wicker?",
             "opts": ["It is light and bends rather than breaks.",
                      "It is colourful and easy to see in the sky.",
                      "It holds the hot air inside the envelope.",
                      "It keeps the gas tanks cool during a flight."],
             "why": "The third paragraph says wicker is light and slightly springy, so it bends rather than breaks on a bumpy landing."},
            {"id": "a4d59837d092", "t": "mcq", "d": "vocab", "q": "“For a quicker descent, the pilot can pull a cord.” Which word or phrase is closest in meaning to descent?",
             "opts": ["way down", "take-off", "change of direction", "landing place"],
             "why": "A descent is a movement downwards: the paragraph is about how the pilot brings the balloon down."},
            {"id": "72a3be2621cc", "t": "mcq", "d": "predict", "q": "A pilot fires the burner for a while and then turns it off. Using the text, what will most likely happen next?",
             "opts": ["The air will slowly cool and the balloon will start to sink.",
                      "The balloon will keep rising higher for the rest of the flight.",
                      "The vent at the top will open by itself to let air out.",
                      "The balloon will turn round and fly back to where it started."],
             "why": "The fourth paragraph says that without the burner the air slowly cools and the balloon sinks."},
            {"id": "68ddc582ef72", "t": "mcq", "d": "structure", "q": "Why does the paragraph about the three main parts come before the paragraph about going up and down?",
             "opts": ["Readers must meet the burner and envelope before learning how they are used.",
                      "The writer thinks the parts are far more interesting than how a balloon flies.",
                      "The writer is telling the events in the order they happened back in 1783.",
                      "The writer wants to persuade readers to go out and buy their own balloon."],
             "why": "The fourth paragraph uses the burner and the envelope to explain rising and sinking, so the reader must meet them first."},
            {"id": "c2d8dc0f1d63", "t": "mcq", "d": "infer", "q": "Using the paragraph about steering, which of these is most likely to be true?",
             "opts": ["A pilot cannot always be sure exactly where the balloon will land.",
                      "Pilots fly only on days when there is no wind at all.",
                      "A balloon always travels in a straight line from start to finish.",
                      "The pilot uses the burner to turn the balloon left or right."],
             "why": "A balloon goes wherever the wind blows it, and the pilot can only change height to find a better wind, so the landing place cannot be fixed in advance."},
        ],
    },
    {
        "key": "RD6.22",
        "year": 6,
        "strand": "Stories",
        "title": "Monsoon on Tilak Lane",
        "nc": "Draw inferences such as inferring characters' feelings, thoughts and motives from their actions; discuss how authors use language",
        "text": (
            "In Mumbai, the monsoon does not arrive politely. One afternoon in June, the sky over Tilak Lane turned "
            "the colour of a bruise, and then the rain came down as if someone had tipped over an enormous "
            "bucket.\n\n"
            "At first, Anjali loved it. She stood on the third-floor balcony with her brother Rohan, watching the "
            "lane below turn into a brown, rushing stream. Rickshaws crawled through it with water up to their "
            "wheels. A man waded past with his trousers rolled to his knees and his shoes held above his head like "
            "a prize.\n\n"
            "Then Anjali noticed the door of the ground-floor flat. Water was sliding under it.\n\n"
            "“That's Mr Kulkarni's,” she said. Mr Kulkarni was eighty-one and walked with a stick. He spent most "
            "mornings on a plastic chair outside his door, reading the newspaper and doing the crossword out "
            "loud.\n\n"
            "The children's mother was at work, but their grandmother was home. She took one look and reached for "
            "her umbrella. “Come,” she said. “Both of you.”\n\n"
            "Downstairs, Mr Kulkarni was standing in an inch of water, trying to lift a metal trunk onto his bed. "
            "His face was tight with effort. “It is nothing,” he insisted. “The water will go down.”\n\n"
            "“Then it can go down while your things are upstairs,” said Grandmother, and that was that.\n\n"
            "For the next hour they carried his belongings up three flights of stairs: blankets, a radio, pots and "
            "pans, a pile of books tied with string. Neighbours appeared from other doors to help. Rohan, who was "
            "nine, took the pots and pans, clanking like a one-boy band. Anjali was trusted with the most precious "
            "thing in the trunk: a bundle of old photographs wrapped in a plastic bag.\n\n"
            "That night, Mr Kulkarni slept on their sofa. By morning the rain had eased, and the lane was a river "
            "of mud. Anjali found him on the balcony, sorting the photographs on his knees.\n\n"
            "“My wife,” he said, pointing to a young woman laughing on a beach. “And this is the house where I was "
            "born. Without you, all of it would have been lost.”\n\n"
            "He looked at Anjali for a long moment. Then he handed her the newspaper, already folded open at the "
            "crossword, and held out his pencil.\n\n"
            "“Seven across,” he said gruffly. “A word that means kindness. I think you will know it.”"
        ),
        "qs": [
            {"id": "4a42f140b6d5", "t": "mcq", "d": "language", "q": "The sky “turned the colour of a bruise”. What does this suggest about the sky?",
             "opts": ["It was dark purple and grey, and threatening.",
                      "It was bright blue, with a few small white clouds.",
                      "It was turning soft pink and gold at sunset.",
                      "It was pale and misty, like an early morning."],
             "why": "A bruise is dark purple, blue and grey, and it comes from being hurt: the sky looks dark and stormy."},
            {"id": "4ecfddbef106", "t": "text", "d": "retrieve", "q": "Where did the man who waded past hold his shoes? Find and copy.",
             "a": ["above his head", "held above his head"],
             "why": "The second paragraph says he held his shoes above his head like a prize."},
            {"id": "830b2a7a667d", "t": "mcq", "d": "infer", "q": "Why did Anjali stop enjoying the rain?",
             "opts": ["She saw that the flood was getting into her neighbour's home.",
                      "Her grandmother told her to come in off the balcony.",
                      "The rickshaws in the lane had stopped moving.",
                      "Rohan had started clanking pots and pans."],
             "why": "“At first” she loved it, but then she noticed water sliding under Mr Kulkarni's door: she realised the rain could do real harm."},
            {"id": "c022cb604510", "t": "mcq", "d": "infer", "q": "Why did Mr Kulkarni say, “It is nothing”?",
             "opts": ["He did not want to admit that he needed help.",
                      "He had already carried his things upstairs.",
                      "He knew the rain was about to stop.",
                      "He wanted to keep the trunk for himself."],
             "why": "He was struggling to lift the trunk, his face tight with effort, yet he said it was nothing: he was too proud to ask for help."},
            {"id": "8e95f6b8c4b7", "t": "tap", "d": "vocab", "q": "Tap the word that means “the things a person owns”.",
             "s": "For the next hour they carried his [belongings] up three flights of stairs: blankets, a radio, pots and pans, a pile of books tied with string.",
             "why": "Belongings are the things that belong to someone: the list after the colon gives some of them."},
            {"id": "3f45ba77c163", "t": "mcq", "d": "retrieve", "q": "What was Anjali trusted to carry?",
             "opts": ["a bundle of old photographs", "the pots and pans",
                      "the metal trunk", "a pile of books tied with string"],
             "why": "Rohan took the pots and pans; Anjali was trusted with the photographs wrapped in a plastic bag."},
            {"id": "1adc57de2c73", "t": "mcq", "d": "infer", "q": "Why does Mr Kulkarni hand Anjali his crossword at the end?",
             "opts": ["to thank her by sharing something he enjoys",
                      "to ask her to finish it because he is too tired",
                      "to keep her busy while he sorts his photographs",
                      "to test whether she is good at spelling"],
             "why": "He has just said his precious photographs would have been lost without her. Sharing the crossword he loves, with a clue about kindness, is his way of thanking her."},
        ],
    },
    {
        "key": "RD6.23",
        "year": 6,
        "strand": "Poems",
        "title": "Before the city wakes",
        "nc": "Discuss and evaluate how authors use language, including figurative language, considering the impact on the reader",
        "text": (
            "At half past four the city is a cat\n"
            "curled tight around itself, one eye half shut.\n"
            "The streetlamps hum their single orange note,\n"
            "and every curtain in the street is drawn.\n\n"
            "The first bus yawns away from the depot,\n"
            "as empty as a lunchbox at home time,\n"
            "its headlights sweeping over shuttered shops\n"
            "like a torch searching for something it has lost.\n\n"
            "On the corner, the baker has been up for hours.\n"
            "His arms are white to the elbow with flour,\n"
            "and the warm breath of his ovens\n"
            "drifts under the door and down the street,\n"
            "telling the pavement a secret: bread.\n\n"
            "A fox trots across the empty market,\n"
            "as businesslike as a postman on his round,\n"
            "checking the bins, the crates, the cardboard,\n"
            "then slipping away between the railings\n"
            "before anyone can ask him where he's going.\n\n"
            "Down by the river, the gulls are up already,\n"
            "bickering over a crust like old neighbours\n"
            "who have forgotten what the quarrel was about.\n\n"
            "On the canal, a narrowboat lies sleeping,\n"
            "its chimney breathing one thin thread of smoke,\n"
            "while a cyclist glides along the towpath,\n"
            "his breath making small clouds in the cold.\n\n"
            "High in a tower block, one light clicks on.\n"
            "Someone is filling a kettle,\n"
            "someone is buttoning a work shirt,\n"
            "someone is standing at the glass\n"
            "to watch the sky turn from ink to grey to gold.\n\n"
            "Then, all at once, the city stretches.\n"
            "Shutters rattle up like waking eyelids.\n"
            "Cars cough. A radio laughs.\n"
            "Footsteps multiply on the station stairs,\n"
            "and the quiet that was here a moment ago\n"
            "is folded up and put away until tonight.\n\n"
            "I like to be awake before all this,\n"
            "to share the streets with just the fox, the baker and the gulls,\n"
            "to know that the city, before it is loud and full,\n"
            "is gentle, and breathes slowly, and dreams a little, just like me."
        ),
        "qs": [
            {"id": "dad471abedf1", "t": "mcq", "d": "language", "q": "The poet writes that at half past four “the city is a cat curled tight around itself”. What does this suggest?",
             "opts": ["The city is quiet and resting, as if asleep.",
                      "The city is full of stray cats at night.",
                      "The city is small and easy to walk round.",
                      "The city is ready to pounce on anyone outside."],
             "why": "A curled-up cat with one eye half shut is dozing: the city is still and sleepy before dawn."},
            {"id": "3a0b8a1eefc6", "t": "text", "d": "retrieve", "q": "Who “has been up for hours”? Find and copy.",
             "a": ["the baker", "baker", "bakers"],
             "why": "The third verse says the baker has been up for hours."},
            {"id": "923fc52af0fa", "t": "mcq", "d": "infer", "q": "“Telling the pavement a secret: bread.” What do these words mean?",
             "opts": ["The smell of baking bread is spreading into the street.",
                      "The baker has dropped some bread on the pavement.",
                      "The baker whispers to people walking past his shop.",
                      "The bread is hidden so that no one can find it."],
             "why": "The “warm breath” of the ovens drifts down the street: it is the smell that tells people bread is being baked."},
            {"id": "2496ef734164", "t": "mcq", "d": "vocab", "q": "“Bickering over a crust like old neighbours.” Which word is closest in meaning to bickering?",
             "opts": ["squabbling", "flying", "sharing", "dozing"],
             "why": "To bicker is to argue about small things: the next line calls it a quarrel."},
            {"id": "5fc2ad65b9fd", "t": "tap", "d": "language", "q": "Tap the word that makes the cars sound like people waking up with a cold.",
             "s": "Cars [cough].",
             "why": "Coughing is something people do, especially first thing in the morning: the cars' engines splutter into life."},
            {"id": "53ee203996c0", "t": "mcq", "d": "structure", "q": "How does the poem change in the verse that begins “Then, all at once”?",
             "opts": ["The quiet city suddenly becomes busy and noisy.",
                      "The poem moves from the city to the countryside.",
                      "Night falls and the city goes back to sleep.",
                      "The speaker leaves home to catch the first bus."],
             "why": "Shutters rattle up, cars cough, footsteps multiply and the quiet is “put away until tonight”: the city wakes up."},
            {"id": "b5d62268817b", "t": "mcq", "d": "infer", "q": "How does the speaker feel about the city before it wakes?",
             "opts": ["They treasure having its quiet streets almost to themselves.",
                      "They feel lonely and wish that everyone would get up.",
                      "They are nervous of the empty, dark streets.",
                      "They prefer it later in the day, when it is loud."],
             "why": "The last verse says “I like to be awake before all this” and calls the early city gentle, like the speaker."},
        ],
    },
    {
        "key": "RD6.24",
        "year": 6,
        "strand": "Play scripts",
        "title": "The 9.15 to Edinburgh",
        "nc": "Prepare play scripts to read aloud and perform; draw inferences about characters' feelings, thoughts and motives",
        "text": (
            "(A busy railway station in London. Above the crowd, a departures board flickers. MUM hurries in, "
            "pulling a suitcase. KEMI, who is eleven, follows with a rucksack. Her brother TUNDE, who is six, "
            "trails behind, eating a banana.)\n"
            "MUM: Platform four, the 9.15. We've got twelve minutes. Kemi, have you got the tickets?\n"
            "KEMI: You've got them, Mum. You said you'd keep them safe.\n"
            "MUM: (stopping dead) Did I? (She pats her coat pockets, then her jeans, then her coat again.) They "
            "were in my hand at the ticket machine. I know they were.\n"
            "TUNDE: Mum, that pigeon's only got one foot.\n"
            "MUM: Not now, Tunde. (She kneels and unzips the suitcase. Socks and jumpers spill out.) Kemi, check "
            "your rucksack.\n"
            "KEMI: (calmly) Let's think. After the ticket machine, we went to the café, and you bought sandwiches.\n"
            "MUM: And then I paid, and then... I don't know! (She looks up at the board.) Ten minutes.\n"
            "TUNDE: Mum, you put something in the sandwich bag.\n"
            "MUM: Tunde, please. Grandma's meeting us at the other end, and if we miss this train...\n"
            "KEMI: Wait. Tunde, what did Mum put in the sandwich bag?\n"
            "TUNDE: (shrugging) Orange papers. She said, “I'll put these somewhere I won't forget.”\n"
            "(A pause. Slowly, MUM reaches into the paper bag on top of the suitcase. She pulls out two orange "
            "tickets, slightly smeared with mayonnaise.)\n"
            "MUM: (half laughing, half groaning) Somewhere I won't forget.\n"
            "KEMI: There should be three.\n"
            "MUM: (shaking the bag) Here. Under the crisps.\n"
            "(A STATION ASSISTANT in a yellow jacket comes over.)\n"
            "ASSISTANT: Everything all right? You look like you're in a hurry.\n"
            "KEMI: We need platform four, for the 9.15.\n"
            "ASSISTANT: You've got seven minutes. Down there, past the clock, on your right. Come on, I'll help you "
            "with those socks.\n"
            "(Together they stuff the clothes back into the suitcase. MUM zips it shut.)\n"
            "MUM: Thank you. Thank you so much.\n"
            "TUNDE: Mum?\n"
            "MUM: (taking his hand, already walking fast) Yes, my clever boy?\n"
            "TUNDE: That pigeon's got two feet really. It was hiding one.\n"
            "(KEMI laughs. They hurry off towards the clock.)"
        ),
        "qs": [
            {"id": "1ef969825d38", "t": "mcq", "d": "retrieve", "q": "At the start of the scene, how long does the family have before the train leaves?",
             "opts": ["twelve minutes", "ten minutes", "seven minutes", "fifteen minutes"],
             "why": "Mum's first line says, “We've got twelve minutes.” Ten and seven minutes are later in the scene."},
            {"id": "39e5260b541b", "t": "mcq", "d": "vocab", "q": "In the stage direction “(stopping dead)”, what does stopping dead mean?",
             "opts": ["stopping suddenly and completely", "stopping because she feels faint",
                      "slowing down little by little", "stopping to have a rest"],
             "why": "To stop dead is to stop all at once: Mum freezes as she realises she may have the tickets."},
            {"id": "542cc8a6bbbc", "t": "mcq", "d": "infer", "q": "Mum pats her coat pockets, then her jeans, then her coat again. What does this show?",
             "opts": ["She is panicking and not thinking clearly.",
                      "She is cold and trying to warm herself up.",
                      "She is pretending to look so Tunde will laugh.",
                      "She knows exactly where the tickets are."],
             "why": "Checking the same coat twice shows she is flustered and searching without a plan."},
            {"id": "4837eb9ac4b1", "t": "mcq", "d": "compare", "q": "How is Kemi's reaction to the lost tickets different from Mum's?",
             "opts": ["Kemi stays calm and thinks back step by step.",
                      "Kemi panics and empties her rucksack on the floor.",
                      "Kemi blames Tunde for losing the tickets.",
                      "Kemi runs off to ask the station assistant."],
             "why": "The stage direction says Kemi speaks calmly, and she goes back over where they went, while Mum is searching wildly."},
            {"id": "32e284d7b855", "t": "mcq", "d": "infer", "q": "Why does Mum repeat “Somewhere I won't forget” half laughing and half groaning?",
             "opts": ["She sees the funny side of forgetting the place she chose.",
                      "She is cross with Tunde for not telling her about it sooner.",
                      "She thinks the mayonnaise has ruined all of the tickets.",
                      "She is copying Tunde's words to make fun of him."],
             "why": "She had chosen the bag so she would not forget it, then forgot it completely: she laughs at herself while still feeling the stress."},
            {"id": "6d9d6f4c3152", "t": "order", "d": "sequence", "q": "Put these events in the order they happen in the scene.",
             "items": ["Mum unzips the suitcase and clothes spill out.",
                       "Tunde says Mum put something in the sandwich bag.",
                       "Mum finds two tickets in the paper bag.",
                       "A station assistant offers to help.",
                       "The family hurry off towards the clock."],
             "why": "Mum searches the suitcase first; Tunde's clue leads to the tickets; then the assistant helps them pack and they set off."},
            {"id": "dbe29b9df97a", "t": "mcq", "d": "structure", "q": "Why does the writer include Tunde's remarks about the pigeon at the start and at the end?",
             "opts": ["They show he notices small things, just as he noticed the tickets.",
                      "They explain why the family very nearly missed their train.",
                      "They show that Tunde was not at all interested in the journey.",
                      "They tell the audience that the station is dirty and crowded."],
             "why": "Tunde spots the pigeon's hidden foot just as he spotted where Mum put the tickets: no one listened to him, but he sees things others miss."},
        ],
    },
    {
        "key": "RD6.25",
        "year": 6,
        "strand": "Information",
        "title": "The canal age",
        "nc": "Distinguish between statements of fact and opinion; retrieve, record and present information from non-fiction",
        "text": (
            "Today, Britain's canals are quiet places. Narrowboats chug slowly past, walkers and cyclists follow "
            "the towpaths, and herons stand like statues at the water's edge. But two hundred and fifty years ago, "
            "these waterways were among the busiest routes in the country.\n\n"
            "In the 1700s, factories and towns were growing fast, and they needed huge amounts of coal, clay, stone "
            "and iron. Moving such heavy loads by road was slow and expensive. Most roads were rough tracks, deep "
            "in mud for much of the year, and a horse pulling a cart could manage only a small load. On calm "
            "water, however, the same horse could pull a boat carrying many times as much.\n\n"
            "In 1761, the Bridgewater Canal opened near Manchester. It had been built for the Duke of Bridgewater "
            "to carry coal from his mines into the city, and its engineer was James Brindley. The canal was such a "
            "success that the price of coal in Manchester fell sharply. Soon, people all over the country wanted "
            "canals of their own, and over the next seventy years or so, thousands of miles of them were dug, "
            "linking rivers, ports, mines and factories.\n\n"
            "Almost all of this digging was done by hand. The workers, called navvies, used picks, shovels and "
            "wheelbarrows. Their name was short for “navigators”, because canals were sometimes called "
            "navigations.\n\n"
            "Canal builders faced one big problem: water lies flat, but land does not. Their main answer was the "
            "lock. A lock is a chamber with gates at each end. To go uphill, a boat enters the lock, the gates "
            "close behind it, and water is let in until the boat has risen to the higher level. Then the gates in "
            "front of it open and the boat carries on. Going downhill, the water is let out instead.\n\n"
            "The canal age did not last. From the 1830s onwards, railways spread across the country, and trains "
            "could carry goods far faster. Many canals fell out of use and became choked with weeds and "
            "rubbish.\n\n"
            "In the last fifty years, however, volunteers and charities have cleared and repaired many of them. "
            "Now people use the canals for holidays, fishing and walking, and they are home to wildlife such as "
            "kingfishers, dragonflies and water voles. In my view, these peaceful waterways are the finest "
            "reminder we have of how our modern world was built."
        ),
        "qs": [
            {"id": "a4a181f2d037", "t": "mcq", "d": "retrieve", "q": "According to the second paragraph, why was moving heavy loads by road so difficult?",
             "opts": ["The roads were rough and muddy, and a cart held only a small load.",
                      "Horses were not allowed to pull carts on the roads near towns.",
                      "The factories were built too far away from any of the roads.",
                      "The roads were already crowded with trains carrying goods."],
             "why": "The second paragraph says most roads were rough tracks, deep in mud, and a horse pulling a cart could manage only a small load. Trains came much later."},
            {"id": "96a5b49ecf6c", "t": "text", "d": "retrieve", "q": "Who was the engineer of the Bridgewater Canal? Find and copy his name.",
             "a": ["James Brindley", "Brindley"],
             "why": "The third paragraph says the canal's engineer was James Brindley. The Duke of Bridgewater was the man it was built for."},
            {"id": "d14d7248318f", "t": "mcq", "d": "infer", "q": "Why do you think the price of coal in Manchester fell after the Bridgewater Canal opened?",
             "opts": ["Coal could now be brought into the city much more cheaply.",
                      "The Duke's mines were running out of coal to sell.",
                      "People in Manchester had stopped burning coal.",
                      "Trains had started to bring coal from further away."],
             "why": "Boats on calm water carry far more than carts on muddy roads, so moving the coal cost less, and it could be sold for less."},
            {"id": "d451a0c5fe50", "t": "mcq", "d": "vocab", "q": "“Many canals fell out of use and became choked with weeds and rubbish.” What does choked mean here?",
             "opts": ["blocked up", "washed clean", "drained dry", "made deeper"],
             "why": "Choked means so clogged that nothing can get through: weeds and rubbish filled the unused canals."},
            {"id": "43f6e2136522", "t": "order", "d": "sequence", "q": "Put these steps in the order they happen when a boat goes uphill through a lock.",
             "items": ["The boat enters the lock.",
                       "The gates close behind the boat.",
                       "Water is let into the lock.",
                       "The gates in front of the boat open."],
             "why": "The fifth paragraph says the boat enters, the gates close behind it, water is let in until it rises, then the gates in front open."},
            {"id": "20c9d92353b4", "t": "mcq", "d": "purpose", "q": "Which of these is an opinion, not a fact?",
             "opts": ["Canals are the finest reminder of how our modern world was built.",
                      "The Bridgewater Canal opened near Manchester in 1761.",
                      "Navvies dug the canals almost entirely by hand.",
                      "Trains could carry goods faster than canal boats."],
             "why": "The writer says “In my view” before calling canals the finest reminder: that is a judgement people could disagree with. The others can be checked."},
            {"id": "9e5896979658", "t": "mcq", "d": "structure", "q": "Which would be the best subheading for the paragraph that begins “The canal age did not last”?",
             "opts": ["Overtaken by the railways", "How a lock works", "The very first canal", "Canals today"],
             "why": "That paragraph explains how railways carried goods faster and canals fell out of use."},
        ],
    },
    {
        "key": "RD6.26",
        "year": 6,
        "strand": "Persuasive writing",
        "title": "Our street needs trees",
        "nc": "Identify how language, structure and presentation contribute to meaning; distinguish between statements of fact and opinion",
        "text": (
            "Walk down Mill Street on a hot July afternoon and you will soon notice something: there is nowhere "
            "to hide from the sun. The pavements bake, the bus stop is like an oven, and the only green thing in "
            "sight is a bench with peeling paint. We, the Year 6 Green Team at Hartfield Primary School, believe "
            "this has to change. Our street needs trees, and we need your help to plant them.\n\n"
            "First, trees keep us cool. A single large tree can shade a whole stretch of pavement, and the water "
            "that evaporates from its leaves cools the air around it, a little like sweat cooling your skin. On "
            "the hottest days, a street lined with trees can feel several degrees cooler than a bare one.\n\n"
            "Second, trees help to keep our air cleaner. Their leaves trap dust and soot from traffic, which the "
            "rain then washes away. Trees also take in carbon dioxide and give out the oxygen that we "
            "breathe.\n\n"
            "Third, trees protect us from flooding. When heavy rain falls on concrete, it rushes straight into the "
            "drains, which can overflow. Tree roots soak up some of that water and help more of it to sink slowly "
            "into the ground.\n\n"
            "And of course, trees are homes. Birds nest in their branches, bees feed on their blossom, and "
            "beetles and spiders shelter in their bark. A large tree can support a whole community of "
            "creatures.\n\n"
            "Some people say that trees are messy, because their leaves fall every autumn. It is true that leaves "
            "need sweeping. But is twenty minutes with a broom really too high a price for shade, cleaner air and "
            "birdsong outside your window? Others worry about the cost. Our school has already raised the money for "
            "the first ten trees, and a local tree charity has offered to plant them for free.\n\n"
            "What we need now is people to look after them. A young tree needs a bucket of water every week "
            "through its first few summers. If every family on Mill Street adopted one tree, the job would be "
            "easy.\n\n"
            "So please join us at our planting morning on the first Saturday in March, and sign up at the school "
            "office to adopt a tree. In fifty years' time, children will walk down a cool, green Mill Street full "
            "of birdsong, and they will have you to thank."
        ),
        "qs": [
            {"id": "1f0798809db9", "t": "mcq", "d": "language", "q": "The writers say “the bus stop is like an oven”. What does this comparison suggest?",
             "opts": ["The bus stop gets uncomfortably hot in summer.",
                      "People cook food while they wait at the bus stop.",
                      "The bus stop is made of shiny metal like an oven.",
                      "People have to wait a very long time for the bus."],
             "why": "An oven is very hot inside: the comparison shows how hot it is waiting at the bus stop with no shade."},
            {"id": "a31ec788c29a", "t": "mcq", "d": "retrieve", "q": "According to the text, how do the leaves of a tree help to keep the air cleaner?",
             "opts": ["They trap dust and soot from traffic.",
                      "They let water evaporate to cool the air.",
                      "They soak up rain before it reaches the drains.",
                      "They shade a whole stretch of pavement."],
             "why": "The third paragraph says the leaves trap dust and soot from traffic. Cooling and shade belong to the paragraph about keeping cool, and roots soak up rain."},
            {"id": "6eaa5d36cfaa", "t": "mcq", "d": "structure", "q": "Why do the writers begin three paragraphs with “First”, “Second” and “Third”?",
             "opts": ["to set out their reasons clearly, one at a time",
                      "to show the order in which the trees will be planted",
                      "to number the first three trees on Mill Street",
                      "to tell the story of how a tree grows up"],
             "why": "Each of those paragraphs gives a different reason for planting trees: keeping cool, cleaner air and less flooding."},
            {"id": "630a81a6ced9", "t": "text", "d": "language", "q": "In the paragraph about flooding, find and copy the word that shows how fast rain runs off concrete.",
             "a": ["rushes", "rushes straight"],
             "why": "“Rushes” shows the water moving fast and with force, straight into the drains."},
            {"id": "cdbb113830f2", "t": "mcq", "d": "language", "q": "“But is twenty minutes with a broom really too high a price for shade, cleaner air and birdsong outside your window?” Why do the writers ask this question?",
             "opts": ["to make the mess seem small next to what trees give",
                      "to find out how long it takes to sweep up leaves",
                      "to ask readers to help sweep the school playground",
                      "to agree that trees really are too messy for streets"],
             "why": "It is a question that expects the answer “no”: twenty minutes of sweeping is set against everything trees give, so the worry about mess looks minor."},
            {"id": "bf46cfcddb25", "t": "mcq", "d": "retrieve", "q": "According to the text, what does the Green Team most need now?",
             "opts": ["families to water and care for the young trees",
                      "money to buy the first ten trees",
                      "a charity that will plant the trees",
                      "people to sweep up the fallen leaves"],
             "why": "The money is already raised and the charity will plant them for free; the seventh paragraph says “What we need now is people to look after them.”"},
            {"id": "53f76c712355", "t": "mcq", "d": "purpose", "q": "Which of these is an opinion, not a fact?",
             "opts": ["Twenty minutes of sweeping is a small price to pay for a tree.",
                      "Tree roots soak up some of the rain that falls.",
                      "The school has raised money for ten trees.",
                      "Some trees drop their leaves in autumn."],
             "why": "Whether sweeping is “a small price” is a judgement people could disagree with. The others can be checked."},
        ],
    },
    {
        "key": "RD6.27",
        "year": 6,
        "strand": "Instructions",
        "title": "How to build a bug hotel",
        "nc": "Retrieve and record information; identify how structure and presentation contribute to meaning",
        "text": (
            "A bug hotel gives insects and other minibeasts a safe place to shelter, feed and spend the winter. "
            "Gardens that are kept very neat often have nowhere for them to hide, so a hotel can make a big "
            "difference. It takes an afternoon to build, and you can make it from things that would otherwise be "
            "thrown away.\n\n"
            "You will need: some old bricks, three or four wooden pallets, a roof tile or a piece of old board, and "
            "plenty of natural filling, such as hollow plant stems, bamboo canes, dry leaves, straw, pine cones, "
            "bark and short logs.\n\n"
            "1. Choose your spot. Find a flat, level patch of ground, ideally in a quiet corner where the hotel "
            "will not be disturbed. A place that gets some sun and some shade suits the widest range of guests.\n"
            "2. Make a firm base. Lay a few bricks on the ground, spaced apart, so that the bottom of the hotel is "
            "raised slightly. This stops the lowest layer from becoming waterlogged.\n"
            "3. Build the floors. Place a pallet on the bricks, then stack the others on top of it. Ask an adult to "
            "help you lift them, as pallets are heavy and may have sharp edges or nails. Do not build the hotel "
            "higher than about a metre.\n"
            "4. Fill the rooms. Pack the gaps between the slats with your natural materials, mixing them up, "
            "because different creatures prefer different rooms. Bundles of hollow stems and bamboo canes are "
            "popular with solitary bees. Dry leaves and straw make cosy winter bedrooms for ladybirds. Damp, "
            "rotting logs at the bottom are ideal for woodlice and beetles.\n"
            "5. Add a roof. Lay the tile or board on top, with a slight slope, so that rain runs off rather than "
            "soaking into the hotel.\n"
            "6. Wait and watch. Some guests will move in within days, but others may take a season or more to "
            "find it. Check on it quietly every few weeks, without pulling the filling out.\n\n"
            "Top tip: do not use any wood that has been painted or treated with chemicals, as these can harm the "
            "very creatures you are trying to help. And if you have space nearby, plant some flowers: guests who "
            "have somewhere to feed are much more likely to stay."
        ),
        "qs": [
            {"id": "6efc5c0ee6e9", "t": "mcq", "d": "purpose", "q": "What is the main purpose of the first paragraph?",
             "opts": ["to explain why a bug hotel is worth building",
                      "to list the materials you will need",
                      "to describe which creatures like which rooms",
                      "to warn readers about sharp nails"],
             "why": "It says what a bug hotel is for and why neat gardens need one, before the list and the steps."},
            {"id": "7756fae2dee6", "t": "mcq", "d": "retrieve", "q": "According to step 2, why should the hotel be raised on bricks?",
             "opts": ["to stop the lowest layer becoming waterlogged",
                      "to make it easier for an adult to lift",
                      "to keep it in the sun for longer each day",
                      "to give the solitary bees somewhere to live"],
             "why": "Step 2 says the bricks raise the bottom of the hotel, and this stops the lowest layer from becoming waterlogged."},
            {"id": "f1c6d6ed1a69", "t": "text", "d": "retrieve", "q": "Which creatures like bundles of hollow stems and bamboo canes? Find and copy two words.",
             "a": ["solitary bees", "solitary bee", "bees"],
             "why": "Step 4 says bundles of hollow stems and bamboo canes are popular with solitary bees."},
            {"id": "bac89515e7a8", "t": "tap", "d": "vocab", "q": "Tap the word that means “perfect” or “exactly right”.",
             "s": "Damp, rotting logs at the bottom are [ideal] for woodlice and beetles.",
             "why": "Ideal means the best possible: rotting logs are just what woodlice and beetles need."},
            {"id": "cb8aa8e41c28", "t": "order", "d": "sequence", "q": "Put these steps in the order the instructions give them.",
             "items": ["Choose a quiet, level spot.",
                       "Lay a few bricks on the ground.",
                       "Stack the pallets on top.",
                       "Pack the gaps with natural materials.",
                       "Lay a tile or board on top as a roof."],
             "why": "The numbered steps go: choose your spot, make a firm base, build the floors, fill the rooms, add a roof."},
            {"id": "c3f2acea06bd", "t": "mcq", "d": "infer", "q": "Why are you told to check the hotel “quietly” and “without pulling the filling out”?",
             "opts": ["so that you do not disturb or harm the creatures inside",
                      "so that the hotel does not become too heavy",
                      "so that the rain can run off the roof properly",
                      "so that you can count the creatures more easily"],
             "why": "The filling is where the guests shelter; noise and pulling it out would disturb them or destroy their rooms."},
            {"id": "b9517b7501e2", "t": "mcq", "d": "retrieve", "q": "Using the top tip, which material should you NOT use?",
             "opts": ["painted wood", "damp, rotting logs",
                      "dry leaves and straw", "an old roof tile"],
             "why": "The top tip says not to use wood that has been painted or treated with chemicals, as it can harm the creatures."},
        ],
    },
    {
        "key": "RD6.28",
        "year": 6,
        "strand": "Stories",
        "title": "The lolly-stick bridge",
        "nc": "Draw inferences such as inferring characters' feelings, thoughts and motives from their actions; make comparisons within a book",
        "text": (
            "The challenge sounded simple when Mr Adeyemi wrote it on the board: build a bridge from lolly sticks "
            "and glue that can cross a gap of thirty centimetres and hold the heaviest load in the class.\n\n"
            "Wen and Amira were partners. Amira had decided what their bridge would look like before Mr Adeyemi "
            "had even finished speaking. “Long and flat,” she said, sketching quickly. “Like the ones on the "
            "motorway. Simple and strong.”\n\n"
            "Wen wasn't so sure, but Amira's drawing looked so confident that he kept quiet. They spent two "
            "lessons gluing sticks side by side into a long, smooth deck, and when it was finished it was the "
            "neatest bridge in the room.\n\n"
            "On testing day, the bridges were placed one at a time between two tables. Mr Adeyemi hung a bucket "
            "from the middle of each and added weights. Their bridge held one weight. It held two. On the third, "
            "it gave a small creak, sagged like a tired hammock and folded in half with a crack that made the "
            "whole class wince.\n\n"
            "Amira stared at the pieces. Her cheeks were scarlet. For the rest of the lesson she didn't say a "
            "word, and when the bell went she pushed the broken bridge into the recycling box without looking at "
            "it.\n\n"
            "The next morning, Wen was waiting at the classroom door with a library book under his arm. “Look,” "
            "he said, opening it at a page of photographs. “Real bridges aren't flat underneath. They've got "
            "triangles. Loads of them.”\n\n"
            "Amira looked for a long time. “Triangles don't bend,” she said slowly. “If you push on a square, it "
            "squashes sideways. A triangle stays a triangle.”\n\n"
            "“Mr Adeyemi said we could have one more go on Friday,” said Wen.\n\n"
            "They started again. This time they built two side walls out of triangles, joined them with cross "
            "pieces and added the deck last. It was messier than their first bridge. Glue oozed from the joints, "
            "and one triangle was definitely wonky. Amira kept wanting to pull it apart and fix it, but Wen "
            "reminded her that wonky did not mean weak.\n\n"
            "On Friday the bucket went on. One weight. Three. Five. The class began to count out loud. At eight, "
            "the bridge gave a creak, and Amira grabbed Wen's sleeve. But it held.\n\n"
            "It was not the strongest bridge in the class: Kofi and Ellie's held nine. But when Mr Adeyemi asked "
            "what everyone had learned, Amira's hand went up first.\n\n"
            "“That the neatest idea isn't always the best one,” she said, “and that you should listen to your "
            "partner, even when he's quiet.”"
        ),
        "qs": [
            {"id": "9c827fb93336", "t": "mcq", "d": "infer", "q": "Why did Wen keep quiet about the first design?",
             "opts": ["Amira seemed so sure of her idea that he did not want to argue.",
                      "He thought a long, flat bridge was the best possible design.",
                      "Mr Adeyemi had told the class not to talk during planning.",
                      "He had not yet read the instructions on the board."],
             "why": "Wen “wasn't so sure”, but Amira's drawing looked so confident that he said nothing."},
            {"id": "00c85b1d4cf6", "t": "mcq", "d": "language", "q": "The first bridge “sagged like a tired hammock”. What does this comparison show?",
             "opts": ["It drooped in the middle under the weight.",
                      "It was soft and comfortable to sit on.",
                      "It swung from side to side in the wind.",
                      "It was hanging from two tall trees."],
             "why": "A hammock dips down in the middle; “tired” adds that the bridge was giving up just before it folded in half."},
            {"id": "3846e9326d51", "t": "mcq", "d": "vocab", "q": "“A crack that made the whole class wince.” Which word or phrase is closest in meaning to wince?",
             "opts": ["flinch", "cheer", "giggle", "whisper"],
             "why": "To wince is to flinch or pull a face as if something hurts: the loud crack made everyone react that way."},
            {"id": "4c2caa775e74", "t": "mcq", "d": "infer", "q": "How did Amira feel after the first test?",
             "opts": ["embarrassed and upset", "relieved and calm",
                      "proud but tired", "bored and impatient"],
             "why": "Her cheeks went scarlet, she said nothing for the rest of the lesson and she pushed the bridge away without looking at it."},
            {"id": "a88d4f412a37", "t": "text", "d": "retrieve", "q": "What did Wen bring to school the next morning? Find and copy.",
             "a": ["a library book", "library book", "the library book", "library books"],
             "why": "Wen was waiting at the classroom door with a library book under his arm."},
            {"id": "d34d3c4e3252", "t": "mcq", "d": "retrieve", "q": "According to Amira, why are triangles useful in a bridge?",
             "opts": ["They keep their shape when they are pushed.",
                      "They use fewer lolly sticks than squares.",
                      "They make the bridge look neater.",
                      "They let the glue dry more quickly."],
             "why": "Amira says triangles don't bend: a square squashes sideways when pushed, but “a triangle stays a triangle”."},
            {"id": "b363cc62d430", "t": "mcq", "d": "compare", "q": "How was the second bridge different from the first?",
             "opts": ["It was messier, but it held far more weight.",
                      "It was neater, and it held the most weight in the class.",
                      "It was flatter, and it was built in half the time.",
                      "It was smaller, so it broke after only two weights."],
             "why": "The first was the neatest but broke on the third weight; the second had oozing glue and a wonky triangle but held eight. Kofi and Ellie's held more."},
            {"id": "2b023ad1a652", "t": "mcq", "d": "summarise", "q": "Which of these best sums up what this story is about?",
             "opts": ["learning from failure and listening to others",
                      "winning a competition by working alone",
                      "a teacher who sets a challenge too hard",
                      "two friends who fall out over a bridge"],
             "why": "The bridge fails, Amira listens to Wen's idea, they improve it, and she says the lesson herself at the end."},
        ],
    },
    {
        "key": "RD6.29",
        "year": 6,
        "strand": "Poems",
        "title": "Great-Grandad's toolbox",
        "nc": "Discuss and evaluate how authors use language, including figurative language; draw inferences from the text",
        "text": (
            "At the back of the shed, in the corner,\n"
            "beneath an old blanket of dust,\n"
            "is Great-Grandad's wooden toolbox,\n"
            "its hinges all freckled with rust.\n\n"
            "He built it himself in Gdańsk, Mum says,\n"
            "when he worked where the great ships were made,\n"
            "and he carried it here on a ferry\n"
            "with nothing but hope and his trade.\n\n"
            "He mended the chairs of the neighbours,\n"
            "he fixed every gate in the street,\n"
            "and he made Mum a dolls' house with windows\n"
            "and stairs for the tiny dolls' feet.\n\n"
            "I lift up the lid, and it groans\n"
            "like a door that's been shut for too long,\n"
            "and the smell that comes out is of sawdust\n"
            "and oil, and it's sharp, and it's strong.\n\n"
            "There's a plane with a blade like a whisper\n"
            "that shaved the pale wood into curls,\n"
            "and a chisel worn smooth at the handle,\n"
            "as smooth as a necklace of pearls.\n\n"
            "There's a tin full of screws and of washers,\n"
            "all sorted by size, every one,\n"
            "and a note in his slanting handwriting\n"
            "that says: “Measure twice. Then cut once.”\n\n"
            "I never once met him. He's only\n"
            "a face in a frame on the stair,\n"
            "a man with a serious moustache\n"
            "and a sprinkle of white in his hair.\n\n"
            "But here, in the dust and the shadows,\n"
            "I can almost see how he would stand:\n"
            "his sleeves rolled up past his elbows,\n"
            "a hammer at rest in his hand.\n\n"
            "Mum says I can have it. I'm nervous.\n"
            "I might spoil it, or lose all the parts.\n"
            "“Tools are for using,” she tells me.\n"
            "“That's how every carpenter starts.”\n\n"
            "So I'm building a box for the blue tits,\n"
            "and nothing fits quite as it should.\n"
            "But the plane and the chisel remember,\n"
            "and they're teaching my hands about wood."
        ),
        "qs": [
            {"id": "9e462fddec57", "t": "mcq", "d": "vocab", "q": "“Its hinges all freckled with rust.” What does freckled mean here?",
             "opts": ["covered in small spots", "broken into pieces",
                      "painted a bright colour", "stiff and hard to move"],
             "why": "Freckles are small brown spots; the rust has made small brown spots all over the hinges."},
            {"id": "ae66bee4db55", "t": "text", "d": "retrieve", "q": "Where did Great-Grandad build the toolbox? Find and copy.",
             "a": ["Gdańsk", "Gdansk", "in Gdańsk", "in Gdansk"],
             "why": "The second verse says he built it himself in Gdańsk."},
            {"id": "86e13e39255b", "t": "mcq", "d": "retrieve", "q": "What did Great-Grandad make for Mum?",
             "opts": ["a dolls' house", "a box for the blue tits", "a wooden toolbox", "a garden gate"],
             "why": "The third verse says he made Mum a dolls' house with windows and stairs. He mended chairs and fixed gates for the neighbours."},
            {"id": "1b82a3224968", "t": "mcq", "d": "language", "q": "The lid “groans like a door that's been shut for too long”. What does this tell you?",
             "opts": ["The lid creaks because it has not been opened for ages.",
                      "The speaker groans because the lid is far too heavy.",
                      "The toolbox has a small wooden door at the front.",
                      "Someone else has been opening the box every day."],
             "why": "Old doors creak when they have been shut a long time; the toolbox has sat under dust and has not been opened for years."},
            {"id": "46f7ec40e920", "t": "mcq", "d": "infer", "q": "What does the chisel “worn smooth at the handle” suggest about Great-Grandad?",
             "opts": ["He used it a great deal over many years.",
                      "He kept it wrapped up and hardly touched it.",
                      "He bought it new just before he died.",
                      "He used it to make jewellery from pearls."],
             "why": "A handle only wears smooth after a hand has held it again and again: he worked with it for a long time."},
            {"id": "6b93fc5bbf0b", "t": "mcq", "d": "infer", "q": "Why is the speaker nervous about being given the toolbox?",
             "opts": ["They are worried about damaging something precious.",
                      "They do not want to work in the dusty shed.",
                      "They think Mum wants to keep it for herself.",
                      "They are frightened of the photograph on the stair."],
             "why": "The speaker says “I might spoil it, or lose all the parts”: the tools matter because they were Great-Grandad's."},
            {"id": "32bed1fc80ce", "t": "mcq", "d": "summarise", "q": "Which best describes the main idea of the last verse?",
             "opts": ["Using the old tools links the speaker to Great-Grandad's skill.",
                      "The speaker has given up because nothing fits properly.",
                      "The speaker would rather buy a bird box from a shop.",
                      "Great-Grandad built the bird box before he died."],
             "why": "Even though nothing fits yet, the tools “remember” and are teaching the speaker's hands, so his skill is passed on."},
        ],
    },
    {
        "key": "RD6.30",
        "year": 6,
        "strand": "News reports",
        "title": "Volunteers turn a new page for library",
        "nc": "Identify how language, structure and presentation contribute to meaning; retrieve and record information",
        "text": (
            "A village library that was due to close for good has been saved, thanks to more than forty volunteers "
            "and a group of determined schoolchildren.\n\n"
            "The library in Carrickmoor, a village in Cumbria, has served the community for over sixty years. In "
            "January, the council announced that it could no longer afford to keep the building open and that it "
            "would close at the end of March. The nearest library would then have been in a town that was a "
            "forty-minute bus journey away.\n\n"
            "The news came as a shock to many. “This is the only place in the village where you can sit somewhere "
            "warm, read the paper and talk to someone, without spending a penny,” said Margaret Doherty, 78, who "
            "has visited the library since she was a girl. “For some older people, it's the only conversation they "
            "have all week.”\n\n"
            "Within a fortnight, a group of parents had called a meeting in the community hall. More than a "
            "hundred people came. Among them were pupils from Carrickmoor Primary School, who handed over a "
            "petition with 1,200 signatures, a remarkable number for a village of fewer than 3,000 people.\n\n"
            "“We do our homework there, and the little ones go to story time on Saturdays,” explained Niamh, 10, "
            "one of the pupils who collected the signatures. “We couldn't just let it disappear.”\n\n"
            "After weeks of talks, the council agreed to hand the building over to a charity set up by the "
            "villagers. The council will go on paying for the heating and lighting for two years, while volunteers "
            "will staff the desk, run the activities and raise money for new books.\n\n"
            "The library reopened last Saturday, when Niamh and Mrs Doherty cut a ribbon together at the door. "
            "Opening hours now include Sunday afternoons, and there are plans for a homework club and a computer "
            "class for older residents.\n\n"
            "Not everyone is sure the arrangement will last. A spokesperson for the council said she admired the "
            "volunteers' energy, but warned that “goodwill alone does not pay the bills for ever”. The charity's "
            "chair, Joseph Mensah, said the group was already planning a summer fair and a sponsored walk. “We know "
            "it won't be easy,” he said. “But this village has shown what it can do.”"
        ),
        "qs": [
            {"id": "dc929249234b", "t": "mcq", "d": "language", "q": "Why does the title of the report say the volunteers “turn a new page”?",
             "opts": ["It plays on the pages of library books and on making a fresh start.",
                      "The volunteers have printed a new page in the village newspaper.",
                      "The volunteers will read a new story to children every Saturday.",
                      "The volunteers have written a new book about the village."],
             "why": "Turning a new page means a fresh start, and pages belong in library books, so the title is a play on words."},
            {"id": "3541b5173a99", "t": "mcq", "d": "structure", "q": "What is the job of the first paragraph of the report?",
             "opts": ["to sum up the main news in one sentence",
                      "to give the opinion of an older resident",
                      "to explain what the council will pay for",
                      "to describe the reopening ceremony"],
             "why": "A news report opens with a short summary of what happened: the library has been saved by volunteers and schoolchildren."},
            {"id": "4054939938ee", "t": "mcq", "d": "retrieve", "q": "When was the library due to close?",
             "opts": ["at the end of March", "in January", "last Saturday", "in two years"],
             "why": "The second paragraph says the council announced in January that it would close at the end of March."},
            {"id": "96cde694bde8", "t": "mcq", "d": "infer", "q": "Why does Margaret Doherty say the library gives some older people “the only conversation they have all week”?",
             "opts": ["Some older people are lonely, and the library is where they meet others.",
                      "Older people are not allowed to talk anywhere else in the village.",
                      "The library runs a talking club for older people every week.",
                      "Older people only visit the library once a week to read."],
             "why": "She describes it as a warm place to talk to someone for free; without it, some older people would have no one to speak to."},
            {"id": "7b84e2fa835b", "t": "text", "d": "retrieve", "q": "How many signatures were on the pupils' petition? Write the number.",
             "a": ["1,200", "1200", "1,200 signatures", "1200 signatures", "one thousand two hundred"],
             "why": "The fourth paragraph says the petition had 1,200 signatures."},
            {"id": "1de165f87004", "t": "order", "d": "sequence", "q": "Put these events in the order they happened.",
             "items": ["The council announced that the library would close.",
                       "Parents called a meeting in the community hall.",
                       "The council agreed to hand the building to a charity.",
                       "Niamh and Mrs Doherty cut a ribbon at the door."],
             "why": "The closure was announced in January; the meeting came within a fortnight; weeks of talks led to the handover; the library reopened last Saturday."},
            {"id": "0fcf86126f7d", "t": "mcq", "d": "compare", "q": "How do the views of the council spokesperson and Joseph Mensah differ at the end?",
             "opts": ["She doubts it can last; he admits it is hard but is hopeful.",
                      "She wants the library closed; he wants it moved to the town.",
                      "She thinks it will be easy; he thinks it is bound to fail.",
                      "She is sure of success; he wants the volunteers to stop."],
             "why": "The spokesperson warns that goodwill does not pay the bills for ever; Mensah says it won't be easy but the village has shown what it can do."},
            {"id": "d63fb9e041ac", "t": "mcq", "d": "predict", "q": "Using the last paragraph, what is the charity most likely to do next?",
             "opts": ["hold events to raise money for the library",
                      "hand the library back to the council",
                      "close the library on Sunday afternoons",
                      "move the library to the community hall"],
             "why": "Joseph Mensah says the group is already planning a summer fair and a sponsored walk: fundraising events."},
        ],
    },
    {
        "key": "RD6.31",
        "year": 6,
        "strand": "Information",
        "title": "Glass: from sand to window",
        "nc": "Retrieve, record and present information from non-fiction; summarise the main ideas drawn from more than one paragraph",
        "text": (
            "Look around you, and you will probably see glass: in windows, mirrors, jars, bottles, spectacles and "
            "the screen of a phone. It is so ordinary that we rarely stop to think about it. Yet glass is made "
            "mainly from one of the most common materials on Earth: sand.\n\n"
            "Sand is made mostly of a substance called silica. If silica is heated to a very high temperature, far "
            "hotter than any kitchen oven, it melts into a thick, glowing liquid. When this liquid cools, it does "
            "not turn back into grains. Instead, it hardens into a clear, solid lump or sheet: glass. To make the "
            "sand melt at a lower temperature, glassmakers mix in soda ash, and they add limestone so that the "
            "finished glass is strong and does not dissolve in water.\n\n"
            "Some glass is made by nature. When a volcano erupts, lava sometimes cools so quickly that it turns "
            "into a shiny black glass called obsidian. Long ago, people chipped obsidian into sharp tools.\n\n"
            "People have been making glass themselves for thousands of years. The ancient Egyptians made small "
            "glass beads and bottles. Later, in Roman times, glassmakers learned to blow glass. A glassblower "
            "gathers a blob of melted glass on the end of a long, hollow pipe and blows into it, like blowing up a "
            "balloon, while turning the pipe to shape the glass. This skill made glass much cheaper, and Roman "
            "homes had glass cups, jugs and even some glass windows.\n\n"
            "For centuries, though, flat window glass was hard to make. It often came out wavy or uneven, with "
            "tiny bubbles trapped inside. Then, in the 1950s, a British engineer called Alastair Pilkington found "
            "a clever solution. He poured melted glass onto a bath of hot liquid tin. The glass floated on the tin "
            "and spread out into a perfectly flat, smooth sheet. This “float glass” method is now used to make "
            "most of the window glass in the world.\n\n"
            "Glass has another great advantage: it can be recycled again and again without wearing out. Old "
            "bottles and jars are crushed, melted and made into new ones. Using recycled glass also saves energy, "
            "because broken glass melts at a lower temperature than raw sand does.\n\n"
            "So the next time you look through a window, remember: you are looking through melted sand."
        ),
        "qs": [
            {"id": "f018d83281b0", "t": "text", "d": "retrieve", "q": "Find and copy the word that names the substance sand is mostly made of.",
             "a": ["silica"],
             "why": "The second paragraph says sand is made mostly of a substance called silica."},
            {"id": "fefbdbc996cf", "t": "mcq", "d": "retrieve", "q": "According to the text, why do glassmakers add limestone?",
             "opts": ["so the glass is strong and does not dissolve in water",
                      "so the sand melts at a lower temperature",
                      "so the glass cools quickly into a sheet",
                      "so the glass turns a shiny black colour"],
             "why": "The second paragraph says limestone makes the finished glass strong and stops it dissolving. Soda ash is what lowers the melting temperature."},
            {"id": "1960aff2f2c9", "t": "mcq", "d": "vocab", "q": "“It is so ordinary that we rarely stop to think about it.” Which word or phrase is closest in meaning to rarely?",
             "opts": ["hardly ever", "never once", "quite often", "very slowly"],
             "why": "Rarely means not often: we hardly ever think about glass because it is everywhere."},
            {"id": "ce770a8f567a", "t": "mcq", "d": "language", "q": "Why does the writer say glassblowing is “like blowing up a balloon”?",
             "opts": ["to help readers picture the glass swelling as air goes in",
                      "to show that the Romans made balloons out of glass",
                      "to explain why glass is a very light material",
                      "to suggest that glassblowing is a game for children"],
             "why": "A balloon swells when you blow into it; the comparison helps readers imagine the blob of melted glass growing into a hollow shape."},
            {"id": "fe7e081d8ecb", "t": "mcq", "d": "compare", "q": "How was window glass made by the float method different from older window glass?",
             "opts": ["It was perfectly flat and smooth instead of wavy.",
                      "It was made from tin instead of from sand.",
                      "It was blown on a pipe instead of poured.",
                      "It was full of bubbles instead of clear."],
             "why": "The fifth paragraph says older glass came out wavy, with bubbles, but float glass spread into a perfectly flat, smooth sheet. The tin was only what it floated on."},
            {"id": "a993ffc71c7b", "t": "mcq", "d": "infer", "q": "Using the text, why might a glass factory prefer to melt old bottles rather than raw sand?",
             "opts": ["Old glass melts at a lower temperature, so it needs less energy.",
                      "Old bottles are already the right shape for new windows.",
                      "Raw sand cannot be turned into clear glass at all.",
                      "Old bottles can be reshaped without being melted."],
             "why": "The sixth paragraph says broken glass melts at a lower temperature than raw sand, so recycling saves energy."},
            {"id": "b4be3be3f4cd", "t": "mcq", "d": "summarise", "q": "Which statement best sums up the main idea of the text?",
             "opts": ["Glass is melted sand, and ways of making it have improved.",
                      "Glass is too wavy and fragile to be useful in our homes.",
                      "The Romans were the first people ever to make glass.",
                      "Volcanoes make most of the glass that we use today."],
             "why": "The text explains how sand becomes glass, then follows people's methods from Egyptian beads to Roman glassblowing, float glass and recycling."},
        ],
    },
    {
        "key": "RD6.32",
        "year": 6,
        "strand": "Stories",
        "title": "The magpie and the mole",
        "nc": "Identify themes and conventions in a wide range of books, including fables; draw inferences about characters' motives",
        "text": (
            "A magpie lived at the top of an ash tree at the edge of a meadow, and she was the proudest bird for "
            "miles around. Her feathers were black and white, with a flash of green and blue when the sun caught "
            "them, and her nest was crammed with treasures: a scrap of silver foil, a bottle top, a broken earring "
            "and a button that shone like a tiny moon.\n\n"
            "Every morning, she sat on the highest branch and called down to the other creatures. “Look at my "
            "riches! Has anyone ever seen such fine things?”\n\n"
            "The rabbits ignored her. The wood pigeons sighed. But one day a young mole, who lived beneath the "
            "meadow and rarely came up into the light, poked his pink nose out of a molehill and asked, “What are "
            "they for?”\n\n"
            "The magpie was astonished. “For? They are not for anything. They are mine. That is enough.”\n\n"
            "The mole thought about this for a while, and then he went back underground.\n\n"
            "That autumn was the wettest anyone could remember. Rain fell for days, and the stream at the bottom of "
            "the meadow burst its banks. Water crept across the grass, and the creatures fled to the hill at the "
            "top of the meadow. The magpie's nest, high in the ash tree, was safe from the flood, but the wind "
            "howled through the branches day and night. Her nest, heavy with treasures and woven loosely to make "
            "room for them, began to shake apart.\n\n"
            "On the third night, a gust tore away one side of it. The bottle top, the button and the earring "
            "tumbled into the brown water below and were gone.\n\n"
            "In the morning, cold and shivering, the magpie flew to the hill where the other creatures had "
            "gathered. There she found the mole, busy at the entrance to a deep, dry tunnel he had dug into the "
            "hillside. Inside, the rabbits were sheltering, and a hedgehog was asleep in a bed of dry grass.\n\n"
            "“You may come in too,” said the mole. “There is room.”\n\n"
            "The magpie hesitated. “I have nothing to give you,” she said quietly. “All my treasures are gone.”\n\n"
            "The mole looked at her with his small, kind eyes. “I did not dig this tunnel to hold treasures,” he "
            "said. “I dug it to hold friends.”\n\n"
            "From that day on, the magpie still liked shiny things. But she wove her nest tightly first, and she "
            "always kept a little space in it for a friend in need."
        ),
        "qs": [
            {"id": "2d4d2a9eaf50", "t": "mcq", "d": "vocab", "q": "“Her nest was crammed with treasures.” Which word or phrase is closest in meaning to crammed?",
             "opts": ["packed full", "decorated", "hidden away", "lined"],
             "why": "Crammed means filled so full that there is hardly room for more."},
            {"id": "c073c5aa69aa", "t": "mcq", "d": "infer", "q": "What does the magpie's calling down every morning show about her?",
             "opts": ["She was boastful and wanted to be admired.",
                      "She was lonely and wanted someone to visit.",
                      "She was generous and wanted to share her things.",
                      "She was worried that someone would steal from her."],
             "why": "She shouts “Look at my riches!” and asks if anyone has seen such fine things: she wants others to admire what she owns."},
            {"id": "a909f97f7bf4", "t": "text", "d": "retrieve", "q": "Which of the magpie's treasures “shone like a tiny moon”? Find and copy one word.",
             "a": ["button", "a button", "the button", "buttons"],
             "why": "The first paragraph describes a button that shone like a tiny moon."},
            {"id": "8b7dfa5b1b38", "t": "mcq", "d": "infer", "q": "Why was the magpie astonished by the mole's question?",
             "opts": ["She had never thought that her treasures needed a use.",
                      "She did not know that moles were able to speak.",
                      "She thought the mole wanted to steal her treasures.",
                      "She could not hear the mole from the top of the tree."],
             "why": "She replies that the treasures are not for anything, they are just hers: the idea of them having a purpose had never occurred to her."},
            {"id": "1d45a0f1a7a9", "t": "mcq", "d": "retrieve", "q": "According to the text, why did the magpie's nest shake apart?",
             "opts": ["It was heavy and loosely woven to make room for her treasures.",
                      "The flood water rose high enough to reach the top of the tree.",
                      "The rabbits had pulled at the branches of the ash tree.",
                      "The mole's tunnel had loosened the roots of the tree."],
             "why": "The sixth paragraph says the nest, heavy with treasures and woven loosely to make room for them, began to shake apart in the wind. It was safe from the flood."},
            {"id": "8cf126104ce0", "t": "order", "d": "sequence", "q": "Put these events in the order they happen in the fable.",
             "items": ["The mole asked what the treasures were for.",
                       "The stream burst its banks.",
                       "The magpie's treasures fell into the water.",
                       "The mole invited the magpie into his tunnel.",
                       "The magpie wove her nest more tightly."],
             "why": "The mole's question came first; the autumn flood followed; the gust took her treasures; the mole offered shelter; afterwards she changed how she built her nest."},
            {"id": "bc1d9302841a", "t": "mcq", "d": "summarise", "q": "Which is the best moral for this fable?",
             "opts": ["Friendship matters more than possessions.",
                      "Always build your home on high ground.",
                      "Never trust a creature who lives underground.",
                      "Treasures are safest when they are well hidden."],
             "why": "The magpie loses her treasures but is saved by the mole's kindness; he dug his tunnel “to hold friends”, and she learns to make room for a friend too."},
        ],
    },
]
