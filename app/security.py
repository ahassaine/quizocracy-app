"""Passwords, PINs, tokens and one-time codes. Standard library only."""
import base64
import hashlib
import hmac
import secrets


def new_id(prefix: str) -> str:
    """Opaque, globally unique, lowercase ids: p_xxxx for pupils, fam_xxxx for families."""
    return f"{prefix}_{secrets.token_hex(8)}"


def hash_secret(secret: str) -> str:
    salt = secrets.token_bytes(16)
    dk = hashlib.scrypt(secret.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)
    return "scrypt$" + base64.b64encode(salt).decode() + "$" + base64.b64encode(dk).decode()


def verify_secret(secret: str, stored: str) -> bool:
    try:
        _, s, d = stored.split("$")
        dk = hashlib.scrypt(secret.encode(), salt=base64.b64decode(s), n=2 ** 14, r=8, p=1, dklen=32)
        return hmac.compare_digest(dk, base64.b64decode(d))
    except Exception:
        return False


def new_token() -> str:
    return secrets.token_urlsafe(32)


def token_key(token: str) -> str:
    """Sessions and links are stored by hash, so a database leak does not leak live tokens."""
    return hashlib.sha256(token.encode()).hexdigest()


def new_code() -> str:
    return f"{secrets.randbelow(10 ** 6):06d}"
