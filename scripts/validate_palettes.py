#!/usr/bin/env python3
"""Validate color identity palette definitions across JSON, CSS, and switcher JS."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PALETTE_COUNT = 8
REQUIRED_TOKENS = {
    "--color-primary-dark",
    "--color-primary-mid",
    "--color-primary-light",
    "--color-secondary",
    "--color-accent",
    "--color-bg",
    "--color-bg-dark",
    "--color-surface",
    "--color-text",
    "--color-text-muted",
    "--color-border",
}
HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


def _load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _parse_css_palettes(path: Path) -> dict[int, dict[str, str]]:
    content = path.read_text(encoding="utf-8")
    palettes: dict[int, dict[str, str]] = {}
    for match in re.finditer(
        r'\[data-palette="(\d+)"\]\s*\{([^}]+)\}', content, re.MULTILINE
    ):
        palette_id = int(match.group(1))
        block = match.group(2)
        tokens = {
            key.strip(): value.strip().rstrip(";")
            for key, value in (
                line.split(":", 1)
                for line in block.splitlines()
                if line.strip() and ":" in line
            )
        }
        palettes[palette_id] = tokens
    return palettes


def _parse_switcher_palettes(path: Path) -> tuple[list[int], dict[int, dict[str, str]]]:
    content = path.read_text(encoding="utf-8")
    ids = [int(value) for value in re.findall(r"\bid:\s*(\d+)", content.split("const PALETTE_TOKENS")[0])]
    tokens: dict[int, dict[str, str]] = {}
    for match in re.finditer(r"(\d+):\s*\{([^}]+)\}", content.split("const PALETTE_TOKENS", 1)[1]):
        palette_id = int(match.group(1))
        block = match.group(2)
        tokens[palette_id] = {
            key.strip().strip('"'): value.strip().strip('"').rstrip(",")
            for key, value in (
                pair.split(":", 1)
                for pair in block.split(",")
                if ":" in pair
            )
        }
    return ids, tokens


def validate_palette_sources() -> list[str]:
    errors: list[str] = []

    json_paths = [
        REPO_ROOT / "color_identity" / "palettes.json",
        REPO_ROOT / "frontend" / "src" / "assets" / "color_identity" / "palettes.json",
    ]
    css_paths = [
        REPO_ROOT / "color_identity" / "palettes.css",
        REPO_ROOT / "frontend" / "src" / "assets" / "color_identity" / "palettes.css",
    ]
    switcher_paths = [
        REPO_ROOT / "page_url" / "shared" / "switcher.js",
        REPO_ROOT / "frontend" / "src" / "assets" / "page_url" / "shared" / "switcher.js",
    ]

    json_data = [_load_json(path) for path in json_paths]
    css_data = [_parse_css_palettes(path) for path in css_paths]
    switcher_data = [_parse_switcher_palettes(path) for path in switcher_paths]

    expected_ids = list(range(1, EXPECTED_PALETTE_COUNT + 1))

    for idx, data in enumerate(json_data):
        palettes = data.get("palettes", [])
        ids = [entry["id"] for entry in palettes]
        if ids != expected_ids:
            errors.append(f"{json_paths[idx]}: expected ids {expected_ids}, got {ids}")
        for entry in palettes:
            missing = REQUIRED_TOKENS - set(entry.get("tokens", {}))
            if missing:
                errors.append(f"{json_paths[idx]} palette {entry.get('id')}: missing tokens {sorted(missing)}")
            for token, value in entry.get("tokens", {}).items():
                if not HEX_RE.match(value):
                    errors.append(f"{json_paths[idx]} palette {entry.get('id')} token {token}: invalid hex {value!r}")

    for idx, palettes in enumerate(css_data):
        if sorted(palettes) != expected_ids:
            errors.append(f"{css_paths[idx]}: expected palette selectors {expected_ids}, got {sorted(palettes)}")
        for palette_id, tokens in palettes.items():
            missing = REQUIRED_TOKENS - set(tokens)
            if missing:
                errors.append(f"{css_paths[idx]} palette {palette_id}: missing tokens {sorted(missing)}")

    for idx, (ids, tokens) in enumerate(switcher_data):
        if ids != expected_ids:
            errors.append(f"{switcher_paths[idx]} PALETTES: expected ids {expected_ids}, got {ids}")
        if sorted(tokens) != expected_ids:
            errors.append(f"{switcher_paths[idx]} PALETTE_TOKENS: expected ids {expected_ids}, got {sorted(tokens)}")

    canonical = json_data[0]["palettes"]
    canonical_by_id = {entry["id"]: entry["tokens"] for entry in canonical}

    for idx, palettes in enumerate(css_data):
        for palette_id, tokens in palettes.items():
            if tokens != canonical_by_id[palette_id]:
                errors.append(f"{css_paths[idx]} palette {palette_id} tokens do not match palettes.json")

    for idx, (_, tokens) in enumerate(switcher_data):
        for palette_id, switcher_tokens in tokens.items():
            if switcher_tokens != canonical_by_id[palette_id]:
                errors.append(f"{switcher_paths[idx]} palette {palette_id} tokens do not match palettes.json")

    if json_data[0] != json_data[1]:
        errors.append("color_identity/palettes.json and frontend copy are out of sync")

    if css_data[0] != css_data[1]:
        errors.append("color_identity/palettes.css and frontend copy are out of sync")

    if switcher_data[0] != switcher_data[1]:
        errors.append("page_url/shared/switcher.js and frontend copy are out of sync")

    return errors


def main() -> int:
    errors = validate_palette_sources()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: validated {EXPECTED_PALETTE_COUNT} palettes across JSON, CSS, and switcher sources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
