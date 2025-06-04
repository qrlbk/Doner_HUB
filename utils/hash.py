# utils/hash.py
"""Password hashing helpers using argon2id."""

from argon2 import PasswordHasher, exceptions
from argon2.low_level import Type

_hasher = PasswordHasher(type=Type.ID)


def hash_pw(password: str) -> str:
    """Return hashed password."""
    return _hasher.hash(password)


def verify(hash_: str, password: str) -> bool:
    """Verify password against existing hash."""
    try:
        return _hasher.verify(hash_, password)
    except exceptions.VerifyMismatchError:
        return False
