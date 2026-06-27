"""
Daily News Agent — discovers cannabis-related news for author review.

Never publishes directly. Output: review queue + agents/output/ log file.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

# Allow imports from backend when run from repo root
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from app.agents.adapter import enqueue_review_item  # noqa: E402
from agents.llm_client import LLMClient  # noqa: E402

AGENTS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = AGENTS_DIR / "output"


def load_config() -> dict:
    config_path = AGENTS_DIR / "config" / "news_sources.yaml"
    return yaml.safe_load(config_path.read_text(encoding="utf-8"))


def run(*, dry_run: bool = False) -> dict:
    """Execute news discovery pipeline."""
    config = load_config()
    client = LLMClient()
    topics = [t["label"] for t in config.get("topics", [])]
    regions = [r["code"] for r in config.get("regions", [])]

    discovered = client.search_news(topics, regions)
    enqueued = []

    for item in discovered[: config.get("max_items_per_run", 20)]:
        if dry_run:
            enqueued.append(item)
            continue
        review = enqueue_review_item(
            item_type="news",
            title=item["title"],
            payload=item,
            source_agent="news_agent",
        )
        enqueued.append(review)

    result = {
        "agent": "news",
        "run_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": dry_run,
        "count": len(enqueued),
        "items": enqueued,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_file = OUTPUT_DIR / f"{date_str}_news.json"
    out_file.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")

    return result


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    summary = run(dry_run=dry)
    print(json.dumps({"count": summary["count"], "output": str(OUTPUT_DIR)}, indent=2))
