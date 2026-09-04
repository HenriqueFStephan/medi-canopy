"""Tests for importing Daily Cannabis digests into the review queue."""

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "backend"))

from import_daily_cannabis_digest import (  # noqa: E402
    default_fixture_for_date,
    import_digest,
    load_digest,
    paper_from_record,
    paper_to_review_payload,
)
from run_daily_cannabis_research import Paper  # noqa: E402

FIXTURE_PATH = REPO_ROOT / "agents" / "fixtures" / "daily_cannabis" / "2026-09-03.json"


def test_fixture_exists_with_twelve_papers():
    payload = load_digest(FIXTURE_PATH)
    assert payload["title"] == "Daily Cannabis 2026-09-03"
    assert len(payload["accepted"]) == 12
    assert payload["issue_number"] == 6


def test_default_fixture_path_for_issue_date():
    assert default_fixture_for_date("2026-09-03") == FIXTURE_PATH


def test_paper_to_review_payload_maps_fields():
    paper = Paper(
        title="CBD trial",
        url="https://doi.org/10.1000/example",
        journal="Test Journal",
        authors="Silva et al.",
        year=2026,
        doi="10.1000/example",
        category="medical",
        summary="A placebo-controlled trial of CBD.",
    )
    payload = paper_to_review_payload(paper)

    assert payload["title"] == "CBD trial"
    assert payload["authors"] == ["Silva et al."]
    assert payload["abstract"] == "A placebo-controlled trial of CBD."
    assert payload["doi"] == "10.1000/example"
    assert payload["published_date"] == "2026-01-01"
    assert payload["keywords"] == ["medical"]


def test_paper_from_record_round_trip():
    record = load_digest(FIXTURE_PATH)["accepted"][0]
    paper = paper_from_record(record)
    assert paper.doi == "10.1016/j.indcrop.2024.120293"
    assert paper.category == "agronomy"
    assert paper.confidence == pytest.approx(0.95)


def test_import_digest_dry_run_does_not_require_queue_write():
    result = import_digest(FIXTURE_PATH, dry_run=True, queue=[])
    assert result["accepted_count"] == 12
    assert result["enqueued_count"] == 12
    assert result["dry_run"] is True
    assert result["items"][0]["payload"]["doi"]


def test_import_digest_skips_duplicate_dois():
    first = load_digest(FIXTURE_PATH)["accepted"][0]
    queue = [{"payload": {"doi": first["doi"]}}]
    result = import_digest(FIXTURE_PATH, dry_run=True, queue=queue)
    assert result["enqueued_count"] == 11
    assert len(result["skipped_duplicates"]) == 1


def test_load_digest_rejects_missing_accepted(tmp_path: Path):
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"title": "x"}), encoding="utf-8")
    with pytest.raises(ValueError, match="accepted"):
        load_digest(bad)
