"""All settings come from the environment, so the service can move to another VM with a copied .env."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def _bool(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    return default if v is None else v.strip().lower() in ("1", "true", "yes", "on")


ENV = os.getenv("QZ_ENV", "dev")                      # dev | test | prod
MONGO_URL = os.getenv("QZ_MONGO_URL", "mongodb://127.0.0.1:27017")
DB_NAME = os.getenv("QZ_DB", "qz_dev")
PUBLIC_URL = os.getenv("QZ_PUBLIC_URL", "http://127.0.0.1:8300").rstrip("/")
COOKIE_SECURE = _bool("QZ_COOKIE_SECURE", PUBLIC_URL.startswith("https://"))
SESSION_DAYS = int(os.getenv("QZ_SESSION_DAYS", "60"))

# Sign-up gate for the beta: when set, a new parent must enter this code.
INVITE_CODE = os.getenv("QZ_INVITE_CODE", "").strip()
# During the beta every new family gets the Family plan for free.
BETA_FAMILY_PLAN = _bool("QZ_BETA_FAMILY_PLAN", True)

# Mail: "smtp" sends through MAIL_HOST (local postfix by default); "capture" stores in the outbox only.
MAIL_MODE = os.getenv("QZ_MAIL_MODE", "capture")
MAIL_HOST = os.getenv("QZ_MAIL_HOST", "localhost")
MAIL_PORT = int(os.getenv("QZ_MAIL_PORT", "25"))
MAIL_FROM = os.getenv("QZ_MAIL_FROM", "Quizocracy <noreply@quizocracy.com>")
# Addresses on these domains are never sent, only captured (used by the end-to-end tests).
CAPTURE_DOMAINS = tuple(d.strip().lower() for d in os.getenv("QZ_CAPTURE_DOMAINS", "example.test").split(",") if d.strip())

TIMEZONE = os.getenv("QZ_TZ", "Europe/London")
SUPPORT_EMAIL = os.getenv("QZ_SUPPORT_EMAIL", "support@quizocracy.com")

PRICE_MONTH = "£3.99"
PRICE_YEAR = "£35"
