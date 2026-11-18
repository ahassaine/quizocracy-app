"""The app's own modules, for tests that check a function directly."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from app.bank import engine  # noqa: E402,F401
from app.maths import maths_engine  # noqa: E402,F401
import app.maths.y6_gen_b  # noqa: E402,F401  (registers the Year 6 generators)
