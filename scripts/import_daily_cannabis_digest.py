#!/usr/bin/env python3
"""
Import a Daily Cannabis digest JSON into the author review queue.

Daily Cannabis GitHub issues carry peer-reviewed paper links that cleared the
reliability filter. This script persists those papers into CanaHub's review
pipeline so the author can approve them for blog publication.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
FIXTURES_DIR = REPO_ROOT / "agents" / "fixtures" / "daily_cannabis"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

if str(REPO_ROOT / "backend") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "backend"))

from run_daily_cannabis_research import Paper  # noqa: E402

from app.agents.adapter import enqueue_review_item  # noqa: E402


def log(message: str, *, error: bool = False) -> None:
    stream = sys.stderr if error else sys.stdout
    print(message, file=stream, flush=True)


def load_digest(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Digest must be a JSON object: {path}")
    accepted = payload.get("accepted")
    if not isinstance(accepted, list):
        raise ValueError(f"Digest has no 'accepted' list: {path}")
    return payload


def paper_from_record(record: dict[str, Any]) -> Paper:
    return Paper(
        title=str(record.get("title") or "").strip(),
        url=str(record.get("url") or "").strip(),
        journal=str(record.get("journal") or "").strip(),
        authors=str(record.get("authors") or "").strip(),
        year=record.get("year"),
        doi=str(record.get("doi") or "").strip(),
        category=str(record.get("category") or "uncategorized").strip(),
        publication_type=str(record.get("publication_type") or "").strip(),
        peer_reviewed=bool(record.get("peer_reviewed")),
        confidence=float(record.get("confidence") or 0.0),
        summary=str(record.get("summary") or "").strip(),
    )


def _parse_authors(authors: str) -> list[str]:
    """Return author list; digest entries use a single 'Name et al.' string."""
    cleaned = authors.strip()
    return [cleaned] if cleaned else []


def paper_to_review_payload(paper: Paper) -> dict[str, Any]:
    """Map a Daily Cannabis Paper into ScientificPaperRaw-compatible payload."""
    authors = _parse_authors(paper.authors)

    keywords = [paper.category] if paper.category and paper.category != "uncategorized" else []
    published_date = f"{paper.year}-01-01" if paper.year else None

    return {
        "title": paper.title,
        "authors": authors,
        "abstract": paper.summary,
        "doi": paper.doi or None,
        "journal": paper.journal or None,
        "published_date": published_date,
        "url": paper.url or None,
        "keywords": keywords,
    }


def existing_doi_keys(queue: list[dict[str, Any]]) -> set[str]:
    keys: set[str] = set()
    for item in queue:
        payload = item.get("payload") or {}
        doi = str(payload.get("doi") or "").strip().lower()
        if doi:
            keys.add(doi)
    return keys


def import_digest(
    digest_path: Path,
    *,
    dry_run: bool = False,
    queue: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    payload = load_digest(digest_path)
    papers = [paper_from_record(record) for record in payload["accepted"] if isinstance(record, dict)]

    if queue is None:
        from app.repositories.json_store import get_review_queue  # noqa: WPS433

        queue = get_review_queue()

    seen = existing_doi_keys(queue)
    enqueued: list[dict[str, Any]] = []
    skipped: list[str] = []

    for paper in papers:
        doi_key = paper.doi.lower() if paper.doi else ""
        if doi_key and doi_key in seen:
            skipped.append(paper.title or doi_key)
            continue
        if doi_key:
            seen.add(doi_key)

        review_payload = paper_to_review_payload(paper)
        if dry_run:
            enqueued.append({"title": paper.title, "payload": review_payload})
            continue

        item = enqueue_review_item(
            item_type="research",
            title=paper.title,
            payload=review_payload,
            source_agent="daily_cannabis",
        )
        enqueued.append(item)

    return {
        "digest": payload.get("title") or digest_path.stem,
        "digest_path": str(digest_path),
        "dry_run": dry_run,
        "accepted_count": len(papers),
        "enqueued_count": len(enqueued),
        "skipped_duplicates": skipped,
        "items": enqueued,
    }


def default_fixture_for_date(date_str: str) -> Path:
    return FIXTURES_DIR / f"{date_str}.json"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Import a Daily Cannabis digest JSON into the review queue."
    )
    parser.add_argument(
        "digest",
        nargs="?",
        default=None,
        help="Path to digest JSON (default: agents/fixtures/daily_cannabis/{date}.json)",
    )
    parser.add_argument("--date", default="2026-09-03", help="Date slug when digest path is omitted")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing queue")
    args = parser.parse_args()

    digest_path = Path(args.digest) if args.digest else default_fixture_for_date(args.date)
    if not digest_path.is_file():
        log(f"Digest not found: {digest_path}", error=True)
        return 2

    try:
        result = import_digest(digest_path, dry_run=args.dry_run)
    except (ValueError, json.JSONDecodeError) as exc:
        log(f"Failed to import digest: {exc}", error=True)
        return 1

    log(
        f"{result['digest']}: enqueued {result['enqueued_count']}/{result['accepted_count']} "
        f"paper(s)"
        + (f", skipped {len(result['skipped_duplicates'])} duplicate(s)" if result["skipped_duplicates"] else "")
    )
    if args.dry_run:
        for item in result["items"]:
            log(f"  [DRY RUN] {item['title']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
