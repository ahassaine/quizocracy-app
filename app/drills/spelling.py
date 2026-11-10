"""Spelling from the national-curriculum statutory lists, with spaced repetition (Leitner boxes)."""
import base64
import datetime
import json
import random
import re

from ..config import BASE_DIR
from ..db import db
from .. import items, progress
from . import typos

LISTS = json.load(open(BASE_DIR / "data" / "nc_spelling.json", encoding="utf-8"))["lists"]
# Years 7-9: no statutory list exists; these are hand-chosen KS3 lists (see the file's "source").
KS3 = json.load(open(BASE_DIR / "data" / "ks3_spelling.json", encoding="utf-8"))["lists"]
INTERVALS = [0, 1, 3, 7, 21]          # days until the next review, by box
LEARNED_BOX = 3                       # three correct answers on separate days
# Other standard British spellings that also count as right (lower case).
VARIANTS = {"coordinates": ("co-ordinates",), "Mr": ("mr.",), "Mrs": ("mrs.",)}

# Every word gets a sentence with a gap, so the child can tell it from words that sound alike
# ("our"/"hour", "accident"/"accidentally"). Written by hand: words the list's year can read, no other
# word from the same list (from Year 3-4 on), and for homophones a sentence that fits only the target.
CUES = {
    # Year 1
    "the": "Look at ___ big dog.", "a": "I have ___ red ball.", "do": "What did you ___ today?",
    "to": "I walk ___ school.", "today": "It is hot ___.", "of": "I ate a bit ___ cake.",
    "said": "Mum ___ yes.", "says": "Dad ___ hello to me every day.", "are": "You ___ my best pal.",
    "were": "We ___ at the park last week.", "was": "It ___ hot yesterday.", "is": "My cat ___ black.",
    "his": "He lost ___ hat.", "has": "The cat ___ four legs.", "I": "___ am happy.",
    "you": "Thank ___ very much.", "your": "Is this ___ bag?", "they": "The boys said ___ were hungry.",
    "be": "I want to ___ a vet.", "he": "Dad said ___ was tired.", "me": "Can you help ___?",
    "she": "My sister said ___ was cold.", "we": "___ went to the park.", "no": "___, thank you.",
    "go": "Let's ___ to the park.", "so": "I am ___ happy!", "by": "Sit ___ me.", "my": "This is ___ dog.",
    "here": "Come over ___.", "there": "Put it over ___.", "where": "___ is my coat?",
    "love": "I ___ my mum.", "come": "Please ___ and play.", "some": "Can I have ___ water?",
    "one": "I have ___ sister.", "once": "Ring the bell just ___.", "ask": "You can ___ the teacher.",
    "friend": "Sam is my best ___.", "school": "We learn at ___.", "put": "___ your coat on.",
    "push": "Can you ___ me on the swing?", "pull": "___ the rope hard!", "full": "My cup is ___ to the top.",
    "house": "We live in a big ___.", "our": "This is ___ car.",
    # Year 2
    "door": "Please shut the ___.", "floor": "The cup fell on the ___.", "poor": "The ___ man had no money.",
    "because": "I am happy ___ it is my birthday.", "find": "Can you ___ my shoe?",
    "kind": "Be ___ to your sister.", "mind": "I don't ___ if it rains.", "behind": "The cat hid ___ the sofa.",
    "child": "Each ___ got a sticker.", "children": "All the ___ ran out to play.",
    "wild": "Lions are ___ animals.", "climb": "Monkeys can ___ trees.", "most": "She scored the ___ goals.",
    "only": "We ___ have ten minutes.", "both": "I need ___ hands to lift it.",
    "old": "My grandad is very ___.", "cold": "Ice is very ___.", "gold": "She won a ___ medal.",
    "hold": "Can you ___ my hand?", "told": "Mum ___ me to tidy up.", "every": "I brush my teeth ___ day.",
    "everybody": "___ clapped at the end of the show.", "even": "Two, four and six are ___ numbers.",
    "great": "We had a ___ day.", "break": "Be careful not to ___ the glass.",
    "steak": "He ate a ___ for dinner.", "pretty": "What a ___ dress.", "beautiful": "The sunset was ___.",
    "after": "We play ___ lunch.", "fast": "A horse can run very ___.", "last": "Z is the ___ letter.",
    "past": "We walked ___ the shop.", "father": "My mother and ___ came to watch.",
    "class": "Our teacher reads to the ___.", "grass": "Cows eat ___.", "pass": "Please ___ me the salt.",
    "plant": "Water the ___.", "path": "Walk along the ___ to the gate.", "bath": "I have a ___ before bed.",
    "hour": "The film lasts an ___.", "move": "Please ___ your chair.", "prove": "Can you ___ it?",
    "improve": "Practice will help you ___.", "sure": "Are you ___?",
    "sugar": "Do you take ___ in your tea?", "eye": "I closed one ___.", "could": "___ you help me?",
    "should": "You ___ wear a coat.", "would": "___ you like some tea?", "who": "___ is at the door?",
    "whole": "She ate the ___ cake.", "any": "Have you got ___ pets?", "many": "How ___ sweets are left?",
    "clothes": "Put your ___ on.", "busy": "The shop is ___ on Saturdays.",
    "people": "Lots of ___ came to the party.", "water": "Fish live in ___.",
    "again": "Can you say that ___?", "half": "I ate ___ of the cake.",
    "money": "I keep my ___ in a piggy bank.",
    "Mr": "Write the short form: ___ Smith is our teacher.", "Mrs": "Write the short form: ___ Patel lives next door.",
    "parents": "My ___ came to the school play.", "Christmas": "___ Day is on 25 December.",
    # Years 3-4
    "accident": "He fell off his bike in an ___.", "accidentally": "I ___ dropped my cup.",
    "early": "I got up ___ to catch the bus.", "knowledge": "She has a good ___ of birds.",
    "purpose": "What is the ___ of this button?", "actual": "The ___ cost was higher than we expected.",
    "actually": "It looked like a frog, but it was ___ a toad.", "earth": "Worms live under the ___.",
    "learn": "At school we ___ to read.", "quarter": "A ___ of 100 is 25.",
    "address": "Write your ___ on the letter.", "eight": "Two fours make ___.",
    "eighth": "She came ___ in the race.", "length": "Measure the ___ of the table.",
    "question": "Put up your hand to ask a ___.", "answer": "Do you know the ___ to the sum?",
    "enough": "Have you had ___ to eat?", "library": "We borrow books from the ___.",
    "recent": "This is a ___ photo of me.", "appear": "Stars ___ in the sky at night.",
    "exercise": "Running is good ___.", "material": "Wool is a soft ___.",
    "regular": "We go to the dentist for ___ check-ups.", "arrive": "What time will the train ___?",
    "experience": "Visiting the zoo was a fun ___.", "medicine": "Take your ___ when you feel ill.",
    "reign": "The queen's ___ was long.", "believe": "I can't ___ how tall you are!",
    "experiment": "In science we did an ___ with ice.", "mention": "Did she ___ the party?",
    "remember": "Can you ___ my name?", "bicycle": "He rides his ___ to school.",
    "extreme": "The desert has ___ heat.", "minute": "Wait a ___.",
    "sentence": "Start every ___ with a capital letter.", "breath": "Take a deep ___.",
    "famous": "She is a ___ singer.", "natural": "It is ___ to feel sad sometimes.",
    "separate": "Put the red and blue beads in ___ boxes.", "breathe": "Try to ___ slowly and calmly.",
    "favourite": "Blue is my ___ colour.", "naughty": "The ___ puppy chewed my shoe.",
    "special": "Today is a ___ day.", "build": "We will ___ a sandcastle.",
    "February": "___ is the shortest month.", "notice": "Did you ___ the new sign?",
    "straight": "Draw a ___ line.", "business": "Her dad runs a small ___.",
    "forward": "Please ___ the email to me.", "forwards": "The car moved ___ and backwards.",
    "occasion": "A wedding is a happy ___.", "occasionally": "We eat out ___, about twice a year.",
    "strange": "What a ___ smell!", "calendar": "Write the date on the ___.",
    "fruit": "An apple is a ___.", "often": "How ___ do you swim?",
    "strength": "It takes ___ to lift a heavy box.", "caught": "She ___ the ball.",
    "grammar": "We study spelling and ___ at school.", "opposite": "Hot is the ___ of cold.",
    "suppose": "I ___ we could go tomorrow.", "centre": "We went to the shopping ___.",
    "group": "Work in a ___ of four.", "ordinary": "It was just an ___ day.",
    "surprise": "The party was a big ___.", "century": "A ___ is 100 years.",
    "guard": "A dog can ___ the house.", "particular": "She likes one ___ song best.",
    "therefore": "It is raining; ___, we will stay inside.", "certain": "Are you ___ the door is locked?",
    "guide": "A ___ showed us round the museum.", "peculiar": "The milk has a ___ smell.",
    "though": "It was cold, even ___ the sun was out.", "although": "___ it was raining, we went out.",
    "circle": "A ___ has no corners.", "heard": "I ___ a noise.", "perhaps": "___ it will snow tomorrow.",
    "thought": "I ___ you were asleep.", "complete": "Did you ___ your homework?",
    "heart": "Your ___ pumps blood.", "popular": "Football is a ___ sport.",
    "through": "We walked ___ the park.", "consider": "Please ___ my idea.",
    "height": "Measure the ___ of the door.", "position": "What ___ do you play in football?",
    "various": "The shop sells ___ kinds of bread.", "continue": "Please ___ reading to the end of the page.",
    "history": "In ___ we find out about the past.", "possess": "Some birds ___ bright feathers.",
    "possession": "This book is my most treasured ___.", "weight": "What is the ___ of the box?",
    "decide": "You can ___ which game to play.", "imagine": "___ you could fly like a bird.",
    "woman": "A ___ helped me cross the road.", "women": "Two ___ were talking at the bus stop.",
    "describe": "Can you ___ what you saw?", "increase": "The price will ___ next year.",
    "potatoes": "We had chips made from ___.", "different": "Twins can look ___ from each other.",
    "important": "It is ___ to wash your hands.", "pressure": "Pump up the tyre to the right ___.",
    "difficult": "This puzzle is very ___.", "interest": "I have a great ___ in space.",
    "disappear": "The sun will ___ behind the clouds.", "island": "An ___ has water all around it.",
    "promise": "I ___ to tidy my room.", "possible": "Is it ___ to swim across the lake?",
    "probably": "It will ___ rain later, so take a coat.",
    # Years 5-6
    "accommodate": "The hotel can ___ fifty guests.", "embarrass": "Please don't ___ me in front of my friends.",
    "persuade": "Can you ___ Mum to let us stay up?", "accompany": "An adult must ___ children under ten.",
    "environment": "We should protect the ___ by recycling.", "physical": "Running is a ___ activity.",
    "according": "___ to the map, the beach is close.", "equip": "We need to ___ the team with new kit.",
    "equipped": "The kitchen is well ___ with pots and pans.", "equipment": "The PE ___ is kept in the shed.",
    "prejudice": "Judging someone by their skin colour is ___.", "achieve": "Work hard and you will ___ your goal.",
    "especially": "I love fruit, ___ strawberries.", "privilege": "Being team captain is a ___.",
    "aggressive": "The ___ dog barked and growled at us.", "exaggerate": "Don't ___ — it wasn't a million miles!",
    "profession": "Teaching is her ___.", "amateur": "He plays for an ___ football club, not for money.",
    "excellent": "Your work is ___!", "programme": "We watched a TV ___.",
    "ancient": "The pyramids are ___ buildings.", "existence": "Dinosaurs went out of ___ long ago.",
    "pronunciation": "Her French ___ is very good.", "apparent": "It soon became ___ that we were lost.",
    "explanation": "The teacher gave a clear ___ of the sum.", "queue": "Wait in the ___.",
    "appreciate": "I ___ your help.", "familiar": "Your face looks ___.",
    "recognise": "I didn't ___ you in your new glasses.", "attached": "A label was ___ to the bag.",
    "foreign": "They went to a ___ country on holiday.", "recommend": "Can you ___ a good book?",
    "forty": "Four tens make ___.", "relevant": "Only write facts that are ___ to the question.",
    "restaurant": "We had dinner at a ___.", "average": "The ___ of 2 and 4 is 3.",
    "frequently": "It rains ___ in Wales.", "awkward": "There was an ___ silence.",
    "government": "The ___ makes the laws of the country.", "rhyme": "Cat and hat ___.",
    "bargain": "Only a pound? What a ___!", "guarantee": "The new phone has a one-year ___.",
    "rhythm": "Clap along to the ___ of the song.", "bruise": "I got a ___ when I banged my knee.",
    "harass": "It is wrong to ___ people online.", "sacrifice": "He made a big ___ to help his family.",
    "category": "Put each animal in the right ___.", "hindrance": "My little brother was more of a ___ than a help.",
    "secretary": "The school ___ answers the phone.", "cemetery": "Flowers were left on the graves in the ___.",
    "identity": "The spy kept her ___ secret.", "shoulder": "She carried her bag on her ___.",
    "committee": "The ___ voted to build a new park.", "immediate": "The fire needed an ___ response.",
    "immediately": "Come here ___!", "signature": "Write your ___ at the bottom of the form.",
    "communicate": "Dolphins ___ with clicks and whistles.", "individual": "Each ___ pupil gets a book.",
    "sincere": "She gave a ___ apology.", "sincerely": "End the letter with 'Yours ___'.",
    "soldier": "The ___ marched in the parade.", "community": "The library is used by the whole ___.",
    "interfere": "Please don't ___ with my game.", "competition": "She won first prize in the ___.",
    "interrupt": "It is rude to ___ when someone is talking.", "stomach": "My ___ hurts after eating too much.",
    "conscience": "His ___ told him to say sorry.", "language": "French is the ___ spoken in France.",
    "sufficient": "Is there ___ food for everyone?", "conscious": "The patient was ___ and talking.",
    "leisure": "Swimming is my favourite ___ activity.", "suggest": "Can you ___ a name for the puppy?",
    "controversy": "The new rule caused a lot of ___.", "lightning": "Thunder and ___ filled the sky.",
    "symbol": "A dove is a ___ of peace.", "convenience": "The shop is open late for our ___.",
    "marvellous": "What a ___ painting!", "system": "The solar ___ has eight planets.",
    "correspond": "The pen pals ___ by letter.", "mischievous": "The ___ kitten unrolled the toilet paper.",
    "temperature": "The ___ dropped below zero.", "criticise": "It is easy to ___ other people's work.",
    "muscle": "Your heart is a ___.", "thorough": "Give your teeth a ___ brush.",
    "curiosity": "Out of ___, she opened the box.", "necessary": "Is it ___ to bring a coat?",
    "twelfth": "December is the ___ month.", "definite": "Is that a ___ yes?",
    "neighbour": "Our ___ lives next door.", "variety": "The shop sells a ___ of sweets.",
    "desperate": "After the walk we were ___ for a drink.", "nuisance": "The buzzing fly was a ___.",
    "vegetable": "A carrot is a ___.", "determined": "She was ___ to win the race.",
    "occupy": "These games will ___ the children for hours.", "vehicle": "A bus is a large ___.",
    "develop": "Tadpoles ___ into frogs.", "occur": "When did the accident ___?",
    "yacht": "They sailed a ___ across the bay.", "dictionary": "Look up the word in a ___.",
    "opportunity": "This trip is a great ___ to learn.", "disastrous": "The flood was ___ for the town.",
    "parliament": "Laws are made in ___.", "available": "Is this seat ___, or is someone sitting here?",
    # KS3 Year 7
    "absence": "Bring a note to explain your ___ from school.", "anxious": "I felt ___ before the test.",
    "apparently": "___, the shop is closed today.", "appearance": "She changed her ___ with a new haircut.",
    "argument": "The brothers had an ___ about the remote.", "atmosphere": "The Earth's ___ is made of gases.",
    "audience": "The ___ clapped at the end of the play.", "autumn": "Leaves fall from the trees in ___.",
    "beginning": "Start reading from the ___ of the book.", "behaviour": "Good ___ earns house points.",
    "biscuit": "I dipped a ___ in my tea.", "ceiling": "A spider hung from the ___.",
    "chocolate": "I had a bar of ___.", "column": "Add up the numbers in each ___.",
    "completely": "The glass was ___ empty.", "cupboard": "The cups are in the kitchen ___.",
    "decision": "It was a hard ___ to make.", "definitely": "I will ___ be there on time.",
    "description": "Write a ___ of your bedroom.", "diagram": "Label the parts of the plant on the ___.",
    "difference": "What is the ___ between 9 and 4?", "disappoint": "I don't want to ___ my team.",
    "discussion": "We had a class ___ about school uniform.", "encourage": "Fans ___ their team by cheering.",
    "extremely": "It was ___ cold on the mountain.", "fierce": "The tiger gave a ___ roar.",
    "generally": "I ___ walk to school, but today I took the bus.", "happened": "What ___ at the party?",
    "heroes": "The firefighters were the ___ of the day.", "imaginary": "My little sister has an ___ friend.",
    "information": "The leaflet gives ___ about the museum.", "interesting": "That was a really ___ book.",
    "listening": "Are you ___ to me?", "lonely": "The new boy felt ___ at break time.",
    "meanwhile": "Mum cooked dinner; ___, Dad set the table.", "nervous": "He was ___ before his first match.",
    "opinion": "In my ___, cats are better than dogs.", "paragraph": "Start a new ___ for a new idea.",
    "quiet": "Please be ___ in the library.", "safety": "Wear a helmet for ___.",
    "science": "In ___ we did an experiment with magnets.", "scissors": "Cut the paper with ___.",
    "speech": "She gave a ___ to the whole school.", "tomorrow": "See you ___!",
    "tongue": "The dog licked me with its ___.", "usually": "I ___ have cereal for breakfast.",
    "Wednesday": "The day after Tuesday is ___.", "whether": "I don't know ___ it will rain.",
    "writing": "Your ___ is very neat.", "adjective": "In 'a red ball', the word red is an ___.",
    "adverb": "In 'she ran quickly', the word quickly is an ___.", "noun": "In 'the cat sat', the word cat is a ___.",
    "verb": "In 'the dog barked', the word barked is a ___.", "pronoun": "'She' and 'they' are each a ___.",
    "preposition": "In 'under the bed', the word under is a ___.", "simile": "'As brave as a lion' is a ___.",
    "metaphor": "'The classroom was a zoo' is a ___.", "apostrophe": "In 'don't', the ___ shows a missing letter.",
    "perimeter": "The ___ is the distance all the way round a shape.",
    "symmetry": "A square has four lines of ___.", "horizontal": "The floor is ___, but the walls are upright.",
    "vertical": "A flagpole stands ___.", "estimate": "Round the numbers to ___ the answer.",
    "diameter": "The ___ of a circle is twice its radius.", "fraction": "One half is a ___.",
    "decimal": "Write one half as a ___: 0.5.", "percentage": "Give your score as a ___, such as 75%.",
    "equation": "Solve the ___ x + 3 = 7.", "oxygen": "We breathe in ___ from the air.",
    "particle": "A tiny ___ of dust floated in the air.", "organism": "A living thing is called an ___.",
    "apparatus": "Set up the ___ for the experiment.", "population": "The ___ of the town is ten thousand.",
    "settlement": "A village is a small ___.", "continent": "Africa is a ___.",
    "chorus": "Everyone sang the ___ of the song.", "sketch": "Draw a quick ___ of the vase.",
    "accurate": "Use a ruler to make your drawing ___.", "advice": "Can you give me some ___?",
    "advise": "I ___ you to wear a coat.", "affect": "Will the rain ___ the match?",
    "effect": "The film had a scary ___.", "audible": "Her voice was barely ___ over the noise.",
    "boundary": "The river forms the ___ between the two fields.", "capital": "Paris is the ___ of France.",
    "climate": "The ___ near the equator is hot all year.",
    "conjunction": "'And', 'but' and 'because' are each a ___.", "coordinates": "The ___ of the point are (3, 4).",
    "currency": "The pound is the ___ of the UK.", "density": "Iron has a greater ___ than water, so it sinks.",
    "evidence": "Use ___ from the text to back up your answer.", "factor": "3 is a ___ of 12.",
    "glossary": "Look up hard words in the ___ at the back of the book.",
    "habitat": "A pond is the ___ of the frog.", "imagery": "The poet uses ___ to help us picture the sea.",
    "landscape": "The painting shows a hilly ___.", "liquid": "Water is a ___ at room temperature.",
    "lyrics": "I know all the ___ of this song.", "mixture": "Sand and water make a ___.",
    "multiple": "12 is a ___ of 3.", "negative": "−5 is a ___ number.", "numerator": "In 3/4, the ___ is 3.",
    "pollution": "Smoke from cars causes air ___.", "positive": "Any number above zero is ___.",
    "prediction": "Make a ___ about how the story will end.", "quotation": "Copy the ___ from the poem exactly.",
    "reaction": "Mixing vinegar and baking soda causes a fizzy ___.",
    "region": "The north-east is a ___ of England.", "reliable": "My old bike is very ___; it never breaks down.",
    "rural": "A farm is in a ___ area.", "solution": "We found a ___ to the problem.",
    "source": "Check the ___ of your facts.", "summary": "Write a short ___ of the story.",
    "theme": "The ___ of the story is friendship.", "vapour": "Water ___ rose from the hot bath.",
    "volcano": "Lava poured out of the ___.",
    # KS3 Year 8
    "absolutely": "I am ___ sure.", "achievement": "Passing the exam was a great ___.",
    "advertisement": "We saw an ___ for a new phone on TV.", "alcohol": "Hand gel contains ___ to kill germs.",
    "analyse": "Scientists ___ the results of the test.", "assessment": "We have a spelling ___ on Friday.",
    "benefit": "Fresh air is a ___ of living by the sea.", "campaign": "The class ran a ___ to stop litter.",
    "character": "The main ___ in the story is a brave girl.",
    "conclusion": "Write a ___ at the end of your essay.", "consequence": "Being late had a ___: I missed the bus.",
    "continuous": "There was a ___ line of cars on the road.",
    "dialogue": "The play is written as a ___ between two friends.",
    "discipline": "Learning an instrument takes ___.", "embarrassed": "I felt ___ when I tripped on stage.",
    "emphasise": "Use bold letters to ___ a key word.", "energy": "Food gives us ___.",
    "evaluate": "___ your work: what went well?", "eventually": "After hours of searching, we ___ found the cat.",
    "except": "Everyone came ___ Tom.", "fortunately": "It rained, but ___ we had umbrellas.",
    "fulfil": "She worked hard to ___ her dream.", "gauge": "The fuel ___ shows the tank is nearly empty.",
    "humorous": "He told a ___ story that made us laugh.", "illustrate": "Draw pictures to ___ your story.",
    "independent": "She is ___ and likes to do things herself.", "jewellery": "Rings and necklaces are ___.",
    "laboratory": "Scientists work in a ___.", "luxury": "A hot bath felt like a real ___.",
    "magazine": "I read a comic ___ every week.", "marriage": "Their ___ took place in June.",
    "mathematics": "Algebra is part of ___.", "misspell": "Check your work so you don't ___ any words.",
    "noticeable": "The stain on his shirt was very ___.", "occurred": "The fire ___ late at night.",
    "parallel": "Railway tracks are ___ lines.", "particularly": "I like sport, ___ tennis.",
    "performance": "The band gave a brilliant ___.",
    "permanent": "Write it in ___ marker so it won't rub off.",
    "persuasion": "With a little ___, Dad agreed to the trip.", "playwright": "Shakespeare was a ___.",
    "preparation": "Good ___ is the key to a good test result.",
    "presence": "Her ___ at the meeting surprised us.", "process": "Making bread is a slow ___.",
    "professional": "She is a ___ footballer who is paid to play.", "receive": "Did you ___ my letter?",
    "reference": "Use a dictionary as a ___ book.", "religious": "Eid and Diwali are ___ festivals.",
    "repetition": "Learning words needs lots of ___.", "research": "Do some ___ on the history of your town.",
    "schedule": "Check the bus ___ for times.", "skilful": "The ___ player dribbled past three defenders.",
    "success": "The bake sale was a big ___.", "technique": "Practise the right swimming ___.",
    "technology": "Phones and computers are modern ___.",
    "unfortunately": "___, the match was cancelled because of rain.", "unnecessary": "Leave out ___ words.",
    "vacuum": "Sound cannot travel through a ___.", "weird": "What a ___ noise!",
    "alliteration": "'Seven slippery snakes' uses ___.", "onomatopoeia": "'Buzz' and 'pop' are examples of ___.",
    "narrator": "The ___ tells the story.", "stanza": "A poem is split into verses, each called a ___.",
    "persuasive": "Write a ___ letter to the head teacher.", "denominator": "In 3/4, the ___ is 4.",
    "perpendicular": "Two lines that meet at a right angle are ___.",
    "circumference": "The ___ is the distance round a circle.",
    "quadrilateral": "A square is a ___ because it has four sides.",
    "isosceles": "An ___ triangle has two equal sides.", "approximately": "The walk takes ___ ten minutes.",
    "hypothesis": "Before the experiment, write your ___.",
    "photosynthesis": "Plants make food from sunlight by ___.",
    "molecule": "A ___ of water is made of hydrogen and oxygen atoms.",
    "nucleus": "The ___ is the control centre of a cell.", "vertebrate": "A fish has a backbone, so it is a ___.",
    "erosion": "The waves cause ___ of the cliffs.", "latitude": "The equator has a ___ of zero degrees.",
    "longitude": "Greenwich has a ___ of zero degrees.",
    "tributary": "A ___ is a small river that joins a bigger one.", "agriculture": "Farming is also called ___.",
    "revolution": "The French ___ began in 1789.", "chronology": "Put the events in order to show the ___.",
    "monarchy": "A country ruled by a king or queen is a ___.", "medieval": "Castles were built in ___ times.",
    "democracy": "In a ___, people vote for their leaders.", "orchestra": "The ___ played at the concert.",
    "melody": "She hummed a sweet ___.", "harmony": "The choir sang in perfect ___.",
    "perspective": "Draw the road in ___ so it gets narrower in the distance.",
    "silhouette": "We saw the dark ___ of a tree against the sunset.", "texture": "Velvet has a soft ___.",
    # KS3 Year 9
    "abbreviation": "'Dr' is an ___ of 'Doctor'.", "acquaintance": "She is not a close friend, just an ___.",
    "acquire": "Try to ___ new skills this year.", "acknowledge": "Please ___ that you got my email.",
    "analysis": "Write an ___ of the poem's language.", "anonymous": "The letter was ___; it had no name on it.",
    "argumentative": "He is very ___ and disagrees with everything.",
    "bureaucracy": "Filling in forms is part of the ___.", "catastrophe": "The earthquake was a ___ for the city.",
    "colleague": "Mum's ___ from work came for dinner.", "commitment": "Joining the team is a big ___.",
    "comparative": "'Bigger' is the ___ form of 'big'.",
    "contemporary": "The gallery shows ___ art made this year.",
    "controversial": "The new rule was ___ and many people disagreed.",
    "correspondence": "Keep all your ___ with the bank.", "deceive": "Don't try to ___ your teacher.",
    "deteriorate": "Without care, the old house will ___.",
    "discrepancy": "There is a ___ between the two totals.",
    "efficient": "An ___ fridge uses less electricity.", "eligible": "You are ___ to vote at 18.",
    "eloquent": "She gave an ___ speech that moved everyone.", "emphasis": "Put the ___ on the first syllable.",
    "entrepreneur": "The young ___ started her own company.", "exhilarate": "Roller coasters ___ and terrify me.",
    "extraordinary": "The view from the top was ___.", "fascinate": "Stars and planets ___ me.",
    "feasible": "Is the plan ___ in the time we have?", "fluorescent": "Cyclists wear ___ jackets to be seen.",
    "foreseeable": "The bridge will be closed for the ___ future.", "gorgeous": "What a ___ sunset!",
    "grievous": "He made a ___ error.", "hierarchy": "In the army there is a strict ___ of ranks.",
    "hygiene": "Washing hands is good ___.",
    "hypocrisy": "Telling others not to litter while dropping litter is ___.",
    "idiosyncrasy": "Wearing odd socks is his ___.", "illegible": "His handwriting is so messy it is ___.",
    "inevitable": "If you never revise, failure is ___.", "intelligence": "Dolphins show great ___.",
    "irrelevant": "That fact is ___ to the question.", "irresistible": "The smell of fresh bread was ___.",
    "liaise": "The teacher will ___ with your parents.", "licence": "You need a driving ___.",
    "maintenance": "The lift is closed for ___.",
    "manoeuvre": "It is hard to ___ a big car into a small space.", "millennium": "A ___ is a thousand years.",
    "miniature": "She collects ___ furniture for her dolls' house.", "necessity": "Water is a ___ for life.",
    "negligible": "The cost was so small it was ___.", "occurrence": "Snow in June is a rare ___.",
    "omission": "The ___ of one word changed the meaning.",
    "parliamentary": "The ___ debate went on late into the night.",
    "perseverance": "With ___, she finally learned to swim.", "personnel": "Hospital ___ wear badges.",
    "phenomenon": "A rainbow is a natural ___.", "possibility": "There is a ___ of rain later.",
    "precede": "A short speech will ___ the film.", "preferred": "She ___ tea to coffee.",
    "prejudiced": "He was ___ against people from other towns.", "prevalent": "Colds are ___ in winter.",
    "proceed": "Please ___ to the exit.", "psychology": "___ is the study of the mind.",
    "questionnaire": "Fill in the ___ about school lunches.",
    "reminiscent": "The smell was ___ of Grandma's kitchen.",
    "resilience": "Bouncing back after a setback shows ___.",
    "rhetorical": "'Who doesn't love holidays?' is a ___ question.",
    "sabotage": "Someone tried to ___ the machine by cutting the wires.",
    "scenario": "Imagine the worst ___ and plan for it.",
    "soliloquy": "In a ___, a character speaks their thoughts alone on stage.",
    "stationary": "The car was ___ at the lights.", "stationery": "Pens and paper are ___.",
    "strategy": "Our team needs a better ___ to win.",
    "subtle": "There is a ___ difference between the two shades.", "successful": "The launch was ___.",
    "supersede": "The new rules ___ the old ones.", "surveillance": "Cameras keep the car park under ___.",
    "susceptible": "Young children are more ___ to colds.",
    "symphony": "The orchestra played a long ___ in four parts.",
    "threshold": "She paused on the ___ before stepping inside.",
    "tragedy": "The sinking of the Titanic was a terrible ___.", "transferred": "She ___ to a new school in May.",
    "tyranny": "The people rose up against the king's ___.", "unanimous": "The vote was ___: everyone agreed.",
    "vicious": "The ___ dog had to be kept on a lead.", "vulnerable": "Baby birds are ___ to cats.",
    "wholly": "I am ___ sure.", "withhold": "Don't ___ information from the police.",
    "chlorophyll": "___ makes leaves green.", "coefficient": "In 5x, the ___ of x is 5.",
    "hypotenuse": "The ___ is the longest side of a right-angled triangle.",
    "trapezium": "A ___ has one pair of parallel sides.", "polygon": "A hexagon is a ___ with six sides.",
    "proportion": "What ___ of the class walk to school?",
    "probability": "The ___ of rolling a six is one in six.", "evaporation": "Puddles dry up because of ___.",
    "condensation": "Water drips down a cold window because of ___.",
    "precipitation": "Rain, snow and hail are kinds of ___.",
    "legislation": "New ___ bans smoking in cars with children.",
    "constitution": "The ___ sets out the basic laws of a country.",
    "Renaissance": "Art flourished in Italy during the ___.",
    "industrial": "Factories grew fast during the ___ Revolution.",
}
# Words that sound like another word, for a school list (a parent's list has no year of its own): a sentence
# that fits only the target, as above. Only where the list's own entry has none (CUES.setdefault below).
SOUND_CUES = {
    "their": "The children put on ___ coats.", "they're": "The twins are here: ___ in the garden.",
    "we're": "___ going to the park after lunch.", "too": "This soup is ___ hot for me.", "two": "I have ___ hands.",
    "wear": "I ___ a coat when it is cold.", "which": "___ way is the park, left or right?",
    "hear": "I can ___ the birds singing.", "you're": "___ my best friend.", "know": "I ___ the answer!",
    "write": "Please ___ your name at the top.", "right": "Turn ___ at the end of the road.",
    "new": "I got ___ shoes for school.", "knew": "I ___ the answer, but I forgot to say it.",
    "went": "Yesterday we ___ to the beach.", "want": "I ___ a drink, please.", "what": "___ is your name?",
    "when": "Come in ___ the bell rings.", "off": "Turn ___ the light.", "then": "First we ate, and ___ we played.",
    "than": "A cat is bigger ___ a mouse.", "for": "This present is ___ you.", "four": "A dog has ___ legs.",
    "won": "Our team ___ the match.", "blue": "The sky is ___.", "blew": "The wind ___ my hat away.",
    "see": "I ___ with my eyes.", "sea": "Fish swim in the ___.", "bee": "A ___ makes honey.",
    "buy": "Can we ___ some sweets at the shop?", "bye": "Say ___ to Grandma.", "whose": "___ coat is this?",
    "who's": "___ coming to the party?", "its": "The dog wagged ___ tail.", "it's": "___ raining again.",
    "quite": "The water is ___ cold, but I can swim.", "piece": "Can I have a ___ of cake?",
    "peace": "After the long war there was ___.", "meet": "Let's ___ at the park.", "meat": "Beef is a kind of ___.",
    "week": "There are seven days in a ___.", "weak": "After being ill, I felt ___.", "night": "Owls hunt at ___.",
    "knight": "The ___ rode a horse and wore armour.", "road": "Look both ways before you cross the ___.",
    "rode": "She ___ her bike to school.", "son": "Their ___ is called Sam.", "sun": "The ___ shines in the sky.",
    "hole": "The dog dug a ___ in the garden.", "seen": "Have you ___ my keys?",
    "scene": "The last ___ of the film made me cry.", "pair": "I need a new ___ of socks.",
    "pear": "A ___ is a green fruit.", "plane": "We flew to Spain on a ___.", "plain": "I like ___ crisps best.",
    "brake": "Press the ___ to stop the bike.", "mail": "The postman brought the ___.",
    "lose": "Don't ___ your gloves.", "loose": "My tooth is ___.", "threw": "She ___ the ball to me.",
    "aloud": "Read the poem ___ to the class.", "allowed": "Are we ___ to play outside?",
    "flour": "We need ___ to bake a cake.", "flower": "A rose is a ___.", "bear": "A brown ___ lives in the woods.",
    "bare": "Walk on the sand with ___ feet.", "herd": "A ___ of cows stood in the field.",
    "tail": "The dog wagged its ___.", "accept": "Please ___ this gift.", "weather": "The ___ is sunny today.",
    "practise": "You need to ___ the piano every day.", "practice": "Football ___ is on Monday.",
    "dessert": "We had ice cream for ___.", "passed": "The bus ___ our house.",
}
for _w, _c in SOUND_CUES.items():
    CUES.setdefault(_w, _c)
# Words that sound alike (or nearly, for a young child: "went"/"want"). A school word in one of these, with no
# sentence of the parent's and none above, gets a short meaning instead (MEANINGS), and the form asks for one.
SOUNDS_LIKE = [
    ("their", "there", "they're"), ("to", "too", "two"), ("where", "wear", "were", "we're"), ("which", "witch"),
    ("hear", "here"), ("your", "you're"), ("know", "no"), ("knew", "new"), ("write", "right"), ("went", "want"),
    ("of", "off"), ("then", "than"), ("for", "four"), ("one", "won"), ("blue", "blew"), ("see", "sea"),
    ("be", "bee"), ("by", "buy", "bye"), ("our", "hour", "are"), ("whose", "who's"), ("its", "it's"),
    ("quite", "quiet"), ("weather", "whether"), ("piece", "peace"), ("meet", "meat"), ("week", "weak"),
    ("night", "knight"), ("road", "rode"), ("sun", "son"), ("whole", "hole"), ("seen", "scene"), ("pair", "pear"),
    ("plain", "plane"), ("great", "grate"), ("break", "brake"), ("steak", "stake"), ("mail", "male"),
    ("tail", "tale"), ("made", "maid"), ("missed", "mist"), ("heard", "herd"), ("passed", "past"),
    ("lose", "loose"), ("threw", "through"), ("aloud", "allowed"), ("flour", "flower"), ("bear", "bare"),
    ("accept", "except"), ("affect", "effect"), ("advice", "advise"), ("practice", "practise"),
    ("stationary", "stationery"), ("desert", "dessert"), ("heal", "heel"), ("berry", "bury"), ("medal", "meddle"),
    ("groan", "grown"), ("fair", "fare"), ("hair", "hare"), ("sail", "sale"), ("wait", "weight"),
    ("waste", "waist"), ("board", "bored"), ("cereal", "serial"), ("what", "want"), ("when", "went"),
]
_SOUNDS = {}
for _g in SOUNDS_LIKE:
    for _w in _g:
        _SOUNDS.setdefault(_w, [])
        _SOUNDS[_w] += [x for x in _g if x != _w and x not in _SOUNDS[_w]]
# The last resort for those with no sentence: what the word means, in a few words (shown as the hint).
MEANINGS = {
    "maid": "a woman who cleans and tidies for a family", "male": "a boy or a man, or a he-animal",
    "tale": "a story", "grate": "to rub food into tiny bits", "stake": "a strong pointed stick",
    "mist": "a thin cloud near the ground", "missed": "did not catch or hit it", "heal": "to get better",
    "heel": "the back of your foot", "berry": "a small round fruit", "bury": "to put deep in the ground",
    "medal": "a prize you wear round your neck", "meddle": "to poke into things that are not yours",
    "groan": "a low, unhappy sound", "grown": "got bigger", "fair": "the same for everyone",
    "fare": "the money for a ride on a bus or train", "hare": "an animal like a big, fast rabbit",
    "hair": "it grows on your head", "sail": "the big cloth that makes a boat go", "sale": "when shop things cost less",
    "wait": "to stay until something happens", "waste": "to use up for nothing; rubbish",
    "waist": "the middle of your body, where a belt goes", "board": "a flat piece of wood",
    "bored": "fed up, with nothing to do", "cereal": "a breakfast food, such as corn flakes",
    "serial": "a story told in parts", "desert": "a hot, dry place with sand", "past": "gone by; after",
    "except": "all but; not counting", "quiet": "with no noise", "whether": "if (whether or not)",
}


def list_for_year(year: int) -> list:
    if year <= 1:
        return LISTS["Y1"]
    if year == 2:
        return LISTS["Y1"] + LISTS["Y2"]
    if year in (3, 4):
        return LISTS["Y3-4"]
    if year in (5, 6):
        return LISTS["Y5-6"]
    return KS3["Y%d" % min(int(year), 9)]


def audio_file(word: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", word.lower()) + ".mp3"


def has_clip(word: str) -> bool:
    return (BASE_DIR / "static" / "audio" / "words" / audio_file(word)).exists()


# ---- the school's weekly list: the parent types or pastes it; for SCHOOL_DAYS it comes before the year list ----
SCHOOL_MAX = 30
SCHOOL_DAYS = 7
SCHOOL_WORD = re.compile(r"[A-Za-z]+(?:['-][A-Za-z]+)*")
_CUE_SPLIT = re.compile(r"\s*[–—]\s*|\s+-\s*|\s*-\s+|\s*:\s*")
_BULLET = re.compile(r"^\s*(?:\d+[.)]|[-•*·–—])\s+")
_KNOWN = {w.lower(): w for lst in list(LISTS.values()) + list(KS3.values()) for w in lst}


def _pieces(text: str) -> list:
    """The parent's text -> [(word, sentence, part)] in order, before any checking. part: the comma-separated
    bit a word came from when that bit had several words, in a line that has commas ("want I want a dog"),
    which is most likely a sentence typed without its dash.

    A sentence starts after a dash or colon that follows a single word ("their - it is their dog"). It runs to
    the end of the line, or to the next comma-separated bit that is a single word: "their - it is their dog,
    should, could" is their (with its sentence), should and could; "when - When I got home, I ate" keeps the
    comma, since "I ate" is more than one word."""
    out = []
    for line in str(text or "").replace("’", "'").replace("‘", "'").splitlines():
        line = _BULLET.sub("", line).strip()
        if not line:
            continue
        parts = [p.strip() for p in re.split(r"\s*[,;]\s*", line)]
        commas = len(parts) > 1
        cue_at = None                            # index in out of the word whose sentence is running
        for part in parts:
            if not part.strip(".!?\"-–— "):
                continue
            m = _CUE_SPLIT.search(part)
            head = part[:m.start()].strip().strip(".!?\"") if m else ""
            if m and m.start() > 0 and SCHOOL_WORD.fullmatch(head):
                out.append([head, part[m.end():].strip(), ""])
                cue_at = len(out) - 1
                continue
            toks = [t for t in part.split() if t.strip(".!?\"-–—")]
            if cue_at is not None and (len(toks) > 1 or "___" in part):
                out[cue_at][1] += ", " + part
                continue
            cue_at = None
            for t in toks:
                out.append([t, "", part if commas and len(toks) > 1 else ""])
    return out


def parse_school_words(text: str) -> tuple[list, str]:
    """The parent's list -> ([{"w": word, "cue": sentence with ___}], error). Words may be split by commas,
    semicolons, new lines or spaces; "there - over there" (or "there: over there") gives a sentence, where the
    word is blanked out, on its own line or in a comma list (see _pieces). Numbered or bulleted lists pasted from
    a school letter are fine."""
    out, seen = [], set()
    for w, cue, _ in _pieces(text):
        w = w.strip(".!?\"")
        w = _KNOWN.get(w.lower(), w)              # "february" is the list's "February", with its own clip
        if not SCHOOL_WORD.fullmatch(w):
            return [], (f"“{w[:30]}” can't be a spelling word: use letters only, with an apostrophe (don't) "
                        "or a hyphen (well-known) if the word has one.")
        if len(w) > 30:
            return [], f"“{w[:30]}…” is too long for one word."
        if w.lower() in seen:
            continue
        seen.add(w.lower())
        cue = cue[:120]
        if cue and "___" not in cue:
            cue = re.sub(r"(?<![A-Za-z'])" + re.escape(w) + r"(?![A-Za-z'])", "___", cue, flags=re.I)
        out.append({"w": w, "cue": cue})
    if len(out) > SCHOOL_MAX:
        return [], (f"That's {len(out)} words. Up to {SCHOOL_MAX} fit in one week's list: "
                    "keep the ones the school sent for this week.")
    return out, ""


def _names(ws: list) -> str:
    """'“I”', '“I” and “a”', '“I”, “a” and “dog”'."""
    q = ["“%s”" % w for w in ws]
    return q[0] if len(q) == 1 else ", ".join(q[:-1]) + " and " + q[-1]


def school_doubts(text: str) -> str:
    """Before saving: a sentence that looks typed without its dash, so its words would become spelling words
    ("went, want I want a dog, what"). Read from how the list is laid out (several words between two commas, or
    a long comma-less line that repeats a word), never from what the words mean. "" when nothing looks wrong."""
    for w, _, part in _pieces(text):
        if part:
            toks = [t.strip(".!?\"") for t in part.split()]
            extra = list(dict.fromkeys(t for t in toks[1:] if t.lower() != toks[0].lower()))[:4]
            look = "looks" if len(extra) == 1 else "look"
            return (f"{_names(extra)} {look} like part of a sentence: did you mean “{toks[0]} - {' '.join(toks[1:])}”? "
                    "Put a dash after the word and the sentence after it, or a comma between words. "
                    "If they really are spelling words, tick “Save the list as it is”.")
    for line in str(text or "").splitlines():
        toks = [t.lower().strip(".!?\"") for t in _BULLET.sub("", line).split()]
        if "," not in line and not _CUE_SPLIT.search(line) and len(toks) >= 5 and len(set(toks)) < len(toks):
            return (f"“{line.strip()[:60]}” looks like it has a sentence in it. Put a comma between words, and a "
                    "sentence after a dash: “there - over there”. If they really are spelling words, tick "
                    "“Save the list as it is”.")
    return ""


def cue_for(word: str, own: str = "") -> tuple[str, str]:
    """The hint a school word gets, and where it comes from: the parent's sentence ("yours"), else our sentence
    ("ours"), else for a word that sounds like another a short meaning ("meaning"), else none ("")."""
    if own:
        return own, "yours"
    if CUES.get(word):
        return CUES[word], "ours"
    if MEANINGS.get(word.lower()):
        return MEANINGS[word.lower()], "meaning"
    return "", ""


def school_summary(words: list, name: str) -> dict:
    """For the form, under the box: what the saved list is, and words that sound like another with no sentence
    of their own ("'their' sounds like 'there': add a sentence so Sam knows which one")."""
    kinds = [cue_for(w["w"], w.get("cue", ""))[1] for w in words]
    ask = []
    for w, k in zip(words, kinds):
        alike = _SOUNDS.get(w["w"].lower())
        if alike and k not in ("yours", "ours"):
            ask.append(f"‘{w['w']}’ sounds like ‘{alike[0]}’: add a sentence after a dash so {name} knows which "
                       f"one, like “{w['w']} - …”.")
    return {"n": len(words), "words": [w["w"] for w in words], "yours": kinds.count("yours"),
            "ours": kinds.count("ours"), "ask": ask[:5]}


def new_school_list(pupil: dict, words: list, start: str, until: str) -> dict:
    """The stored list. "before": the words of earlier lists, so the parent sees last week's tricky ones and they
    keep coming back in practice (carried_words)."""
    sl = pupil.get("school_words") or {}
    now = {w["w"].lower() for w in words}
    before = [w["w"] for w in sl.get("words") or []] + list(sl.get("before") or [])
    before = [w for w in dict.fromkeys(before) if w.lower() not in now][:60]
    return {"words": words, "from": start, "until": until, "before": before}


def carried_words(pupil: dict) -> list:
    """Words of earlier school lists (and of a list whose week is over): still practised when due, like the
    year list's words, until learned."""
    sl = pupil.get("school_words") or {}
    running = {w["w"].lower() for w in school_words(pupil)}
    names = ([] if running else [w["w"] for w in sl.get("words") or []]) + list(sl.get("before") or [])
    return [w for w in dict.fromkeys(names) if w.lower() not in running]


def school_text(words: list) -> str:
    """The list as the form shows it again: one word a line, with its sentence after a dash."""
    return "\n".join(w["w"] + (" - " + w["cue"] if w.get("cue") else "") for w in words)


def school_words(pupil: dict, day: str | None = None) -> list:
    """The school list while it runs (from its first day for SCHOOL_DAYS, or until replaced), else []."""
    sl = pupil.get("school_words") or {}
    day = day or progress.today()
    if not sl.get("words") or not (sl.get("from", "") <= day < sl.get("until", "")):
        return []
    return sl["words"]


def _school_cue(pupil: dict, word: str) -> str:
    cue = next((w.get("cue", "") for w in school_words(pupil) if w["w"].lower() == word.lower()), "")
    return cue_for(word, cue)[0]


async def school_status(pupil: dict) -> dict | None:
    """For the parent: each word of the running school list and how far it is learned, and words of earlier
    lists not yet learned that were spelt wrong ("still tricky")."""
    words = school_words(pupil)
    if not words:
        return None
    old = carried_words(pupil)
    state = {d["word"].lower(): d async for d in db.spelling_words.find(
        {"pupil_id": pupil["_id"], "word": {"$in": [w["w"] for w in words] + old}})}
    last_tricky = [w for w in old if (st := state.get(w.lower())) and st.get("wrong")
                   and int(st.get("box", 0)) < LEARNED_BOX]
    out = []
    for w in words:
        st = state.get(w["w"].lower())
        box = int(st.get("box", 0)) if st else -1
        out.append({"word": w["w"], "state": "learned" if box >= LEARNED_BOX else "right" if box > 0
                    else "tricky" if st else "new", "right": int(st.get("right", 0)) if st else 0})
    sl = pupil["school_words"]
    return {"words": out, "learned": sum(1 for w in out if w["state"] == "learned"), "total": len(out),
            "until": sl["until"], "last_tricky": last_tricky}


def _today() -> datetime.date:
    return datetime.date.fromisoformat(progress.today())


async def next_question(pupil: dict, focus: str | None = None) -> dict:
    """focus: a word to spell again (a mistake being put right)."""
    words = list_for_year(pupil.get("year", 3))
    state = {d["word"]: d async for d in db.spelling_words.find({"pupil_id": pupil["_id"]})}
    last = (pupil.get("_last_spelling") or "")
    today = _today().isoformat()
    shown = await items.just_shown(pupil, "spelling")     # a missed word comes back later, not straight away
    carried = [w for w in carried_words(pupil) if w not in words]     # earlier school lists: due ones come back
    due = [w for w in words + carried if w in state and state[w].get("due", "") <= today and w != last and w not in shown]
    new = [w for w in words if w not in state]
    # the school's list comes first: its new words, and those due today (a missed one after its gap)
    school = [w["w"] for w in school_words(pupil)]
    school_due = [w for w in school if w != last and w not in shown
                  and (w not in state or state[w].get("due", "") <= today)]
    if focus and (has_clip(focus) or focus in school):
        word = focus
    elif school_due:
        word = min(school_due, key=lambda w: (state[w].get("box", 0) if w in state else 0, school.index(w)))
    elif due:
        due.sort(key=lambda w: (state[w].get("box", 0), state[w].get("due", "")))
        word = due[0]
    elif new:
        word = new[0]
    else:
        word = random.choice([w for w in words if w != last and w not in shown] or [w for w in words if w != last] or words)
    cue = _school_cue(pupil, word) if word in school else CUES.get(word, "")
    token = await items.issue(pupil, "spelling", word, {"cue": cue, "school": word in school})
    await db.pupils.update_one({"_id": pupil["_id"]}, {"$set": {"_last_spelling": word}})
    q = {"token": token, "audio": f"/api/spelling/audio/{token}", "cue": cue, "letters": len(word)}
    if not has_clip(word):
        # a school word with no recorded clip: the browser's voice says it (sent encoded, not as plain text)
        q.update({"audio": "", "say": base64.b64encode(word[::-1].encode()).decode()})
    return q


async def check(pupil: dict, token: str, value: str, ms: int | None) -> dict | None:
    it = await items.claim(pupil, "spelling", token)
    if not it:
        return None
    word = it["answer"]
    typed = " ".join(str(value or "").split()).lower()
    correct = typed == word.lower() or typed in VARIANTS.get(word, ())
    if correct and word in await items.just_shown(pupil, "spelling"):
        # right, but straight after being shown it: counts for today, not as learned or as a mistake put right
        await progress.record(pupil, "spelling", correct, ms, "", "Spell the word you heard", word, value)
        return {"correct": True, "expected": word, "again_later": True}
    st = await db.spelling_words.find_one({"_id": f"{pupil['_id']}:{word}"}) or {}
    box = int(st.get("box", 0))
    box = min(box + 1, len(INTERVALS) - 1) if correct else 0
    days = INTERVALS[box] if correct else 0
    if box < LEARNED_BOX and word in {w["w"] for w in school_words(pupil)}:
        days = min(days, 1)                   # a school word comes back every day of its week until it is learned
    due = (_today() + datetime.timedelta(days=days)).isoformat()
    await db.spelling_words.update_one({"_id": f"{pupil['_id']}:{word}"}, {
        "$set": {"pupil_id": pupil["_id"], "family_id": pupil["family_id"], "word": word, "box": box, "due": due},
        "$inc": {"right" if correct else "wrong": 1}}, upsert=True)
    await progress.record(pupil, "spelling", correct, ms, word, "Spell the word you heard", word, value)
    out = {"correct": correct, "expected": word}
    if not correct and typed:
        # which letters were wrong, not only the right spelling: "acsident → accident: cs should be cc"
        if typos.american(word, typed):
            out["hint"] = "That's the American spelling — in the UK we write %s." % word
        else:
            hint = typos.letter_hint(typed, word.lower())
            if hint:
                out["hint"] = hint
                out["marks"] = typos.letter_marks(typed, word.lower())
    return out


async def learned_count(pupil: dict) -> dict:
    words = list_for_year(pupil.get("year", 3))
    n = await db.spelling_words.count_documents({"pupil_id": pupil["_id"], "box": {"$gte": LEARNED_BOX},
                                                 "word": {"$in": words}})
    return {"learned": n, "total": len(words)}
