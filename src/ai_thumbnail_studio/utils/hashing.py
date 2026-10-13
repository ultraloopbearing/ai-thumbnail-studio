"""Stable short hashes for prompt/seed dedup keys."""
from __future__ import annotations

import hashlib


def short_hash(value: str, length: int = 12) -> str:
    if length < 4 or length > 40:
        raise ValueError("length must be in [4, 40]")
    return hashlib.sha1(value.encode("utf-8")).hexdigest()[:length]