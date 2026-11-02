"""Every school year has a spelling list, every word has its audio clip, and no word repeats within a list."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.drills.spelling import CUES, audio_file, list_for_year  # noqa: E402

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
