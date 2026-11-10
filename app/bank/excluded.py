"""Bank content left out of the app because some families object to the topic (Ali, 10 Nov 2026: avoid
evolution and the sensitive PSHE topics altogether). The content files stay as written; engine.load() skips
what is listed here, so a child never meets it and it counts nowhere (mastery, strands, the parent's pages).
Taking a line out brings the content back."""

# Whole skills.
SKILLS = {
    "SC6.16",   # Evolution and natural selection
    "SC9.09",   # Natural selection and evolution
    "SC7.16",   # Male and female reproductive systems
    "SC7.17",   # Gametes and the menstrual cycle
    "SC7.18",   # Fertilisation and gestation
    "SC7.19",   # The placenta, the mother's lifestyle and birth
}

# Single questions in skills that otherwise stay, by skill key and question text ("q").
QUESTIONS = {
    "SC5.06": {     # How humans change as they grow older: puberty and periods out; growth, gestation and old age stay
        "What is the name for the time when a child's body starts changing into an adult's body?",
        "At about what age does puberty usually start?",
        "Which change happens to both boys and girls during puberty?",
        "Which change usually happens only to boys during puberty?",
        "Which change usually happens only to girls during puberty?",
        "Why do the body changes in puberty happen?",
        "Why does puberty start at different ages for different people?",
    },
    "SC7.11": {     # Specialised cells: the human sperm and egg cells out; nerve, muscle, root hair and the rest stay
        "How is a sperm cell adapted to reach the egg?",
        "Why is an egg cell much larger than a sperm cell?",
        "Which specialised cell has a tail and carries genetic material to the egg?",
        "Why does a sperm cell have lots of mitochondria?",
        "What is special about the membrane of an egg cell after fertilisation?",
        "The tip of a sperm cell's head contains enzymes. What are they for?",
        "A typical human egg cell is about 0.1 mm across and a sperm head is about 0.005 mm across. How many times "
        "wider is the egg?",
        "Which specialised cell is the female gamete and has a large food store?",
    },
}
