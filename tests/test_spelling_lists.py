"""Every school year has a spelling list, every word has its audio clip, and no word repeats within a list."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.drills.spelling import CUES, KS3, LISTS, audio_file, list_for_year  # noqa: E402

AUDIO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "static", "audio", "words")


def test_every_year_has_words_with_audio():
    for year in range(1, 10):
        words = list_for_year(year)
        assert len(words) >= 40, year
        assert len({w.lower() for w in words}) == len(words), year
        missing = [w for w in words if not os.path.exists(os.path.join(AUDIO, audio_file(w)))]
        assert not missing, (year, missing[:10])


def test_cues_have_one_gap():
    assert all(c.count("___") == 1 for c in CUES.values())


def test_every_word_has_a_cue_without_the_word():
    for name, words in list(LISTS.items()) + list(KS3.items()):
        for w in words:
            cue = CUES.get(w, "")
            assert cue.count("___") == 1, (name, w, cue)
            assert w.lower() not in re.findall(r"[a-z]+", cue.lower()), (name, w, cue)


def test_cues_do_not_spell_other_words_from_the_list():
    # Years 1-2 lists are mostly little words ("the", "is", "my") that every sentence needs.
    for name, words in [(k, v) for k, v in LISTS.items() if k not in ("Y1", "Y2")] + list(KS3.items()):
        for w in words:
            toks = set(re.findall(r"[a-z]+", CUES[w].lower()))
            assert not [o for o in words if o != w and o.lower() in toks], (name, w, CUES[w])
