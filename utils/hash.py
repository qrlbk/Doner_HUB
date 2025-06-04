"""# utils/hash.py
Argon2id password hashing utilities."""
from argon2 import PasswordHasher

_hasher = PasswordHasher(type="ID")


def hash_password(password: str) -> str:
    """Hash password using Argon2id."""
    return _hasher.hash(password)


def verify_password(hash_: str, password: str) -> bool:
    """Verify password against hash."""
    try:
        _hasher.verify(hash_, password)
        return True
    except Exception:
        return False
