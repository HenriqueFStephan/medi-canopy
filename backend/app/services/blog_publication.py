"""Helpers for blog post publication dates (display + sort)."""

from __future__ import annotations

import re

from app.models.schemas import ContentSource

_YEAR_MONTH = re.compile(r"^\d{4}-\d{2}$")
_YEAR_ONLY = re.compile(r"^\d{4}$")


def normalize_publication_date(value: str | None) -> str | None:
    """Normalize partial dates (YYYY, YYYY-MM) to ISO YYYY-MM-DD for sorting/display."""
    if not value:
        return None
    cleaned = value.strip()
    if not cleaned:
        return None
    if _YEAR_ONLY.match(cleaned):
        return f"{cleaned}-01-01"
    if _YEAR_MONTH.match(cleaned):
        return f"{cleaned}-01"
    return cleaned


def resolve_publication_date(item: dict) -> str | None:
    """
    Return the date used for list display and sorting.

    Research posts use the scholarly publication date. Other posts fall back to
    ``published_at`` (site publication time).
    """
    normalized = normalize_publication_date(item.get("published_date"))
    if normalized:
        return normalized
    if item.get("source_type") == ContentSource.AGENT_RESEARCH.value:
        return None
    published_at = item.get("published_at")
    if not published_at:
        return None
    return str(published_at)[:10]


def publication_sort_key(item: dict) -> str:
    """
    Sort key: newest publication date first (use with ``reverse=True``).

    Items without a publication date sort last and do not affect ordering among
    dated items.
    """
    return resolve_publication_date(item) or ""
