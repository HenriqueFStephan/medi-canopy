"""Demo JSON store reseeds when committed seed files change."""

import json
from pathlib import Path

from app.repositories.json_store import JsonStore


def _write(path: Path, payload: list[dict]) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_reseeds_when_live_store_differs_from_new_seed(tmp_path: Path):
    seed = tmp_path / "seed.json"
    live = tmp_path / "live.json"
    _write(seed, [{"id": "a", "title": "New"}])
    _write(live, [{"id": "a", "title": "01 — Old"}])

    store = JsonStore(live, seed)

    assert store.read_all() == [{"id": "a", "title": "New"}]


def test_keeps_live_data_when_seed_unchanged(tmp_path: Path):
    seed = tmp_path / "seed.json"
    live = tmp_path / "live.json"
    items = [{"id": "a", "title": "Same"}]
    _write(seed, items)
    _write(live, items)

    JsonStore(live, seed)
    _write(live, [{"id": "a", "title": "Edited at runtime"}])

    store = JsonStore(live, seed)

    assert store.read_all() == [{"id": "a", "title": "Edited at runtime"}]


def test_reseeds_after_seed_file_changes(tmp_path: Path):
    seed = tmp_path / "seed.json"
    live = tmp_path / "live.json"
    _write(seed, [{"id": "a", "title": "First"}])
    JsonStore(live, seed)

    _write(seed, [{"id": "a", "title": "Second"}])
    store = JsonStore(live, seed)

    assert store.read_all() == [{"id": "a", "title": "Second"}]
