"""The app's own modules, for tests that check a function directly."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from app.bank import engine  # noqa: E402,F401
