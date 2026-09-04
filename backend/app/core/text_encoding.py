"""Repair UTF-8 text that was decoded as Windows-1252 / Latin-1 (mojibake).

Portuguese copy like "Regulamentação" is stored as UTF-8. If those bytes are
read as cp1252, the string becomes "RegulamentaÃ§Ã£o". One round-trip through
cp1252 → UTF-8 restores the original characters.

Already-correct Unicode is left unchanged: encoding as cp1252 then decoding as
UTF-8 fails for real Portuguese letters (e.g. U+00E7), so we keep the input.
"""

from __future__ import annotations

from typing import Any

_MOJIBAKE_HINTS = ("Ã", "Â", "â€")


def repair_mojibake_text(value: str) -> str:
    """Return `value` with a single UTF-8/cp1252 mojibake layer removed."""
    if not value or not any(hint in value for hint in _MOJIBAKE_HINTS):
        return value
    try:
        repaired = value.encode("cp1252").decode("utf-8")
    except UnicodeError:
        return value
    return repaired if repaired else value


def repair_mojibake(value: Any) -> Any:
    """Recursively repair strings inside JSON-compatible structures."""
    if isinstance(value, str):
        return repair_mojibake_text(value)
    if isinstance(value, list):
        return [repair_mojibake(item) for item in value]
    if isinstance(value, dict):
        return {key: repair_mojibake(item) for key, item in value.items()}
    return value
