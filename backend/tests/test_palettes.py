"""Tests for color identity palette definitions."""

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from validate_palettes import EXPECTED_PALETTE_COUNT, validate_palette_sources


def test_palette_sources_are_consistent():
    errors = validate_palette_sources()
    assert errors == [], "\n".join(errors)


def test_expected_palette_count():
    assert EXPECTED_PALETTE_COUNT == 8
