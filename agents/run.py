"""
Agent CLI — manual and scheduled entry point.

Usage:
    python -m agents.run --agent news
    python -m agents.run --agent research
    python -m agents.run --agent all --dry-run
"""

import argparse
import json
import sys
from pathlib import Path

# Ensure repo root on path
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def main() -> None:
    parser = argparse.ArgumentParser(description="Medi Canopy agent runner")
    parser.add_argument(
        "--agent",
        choices=["news", "research", "all"],
        required=True,
        help="Which agent to run",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write to review queue",
    )
    args = parser.parse_args()

    results = []

    if args.agent in ("news", "all"):
        from agents.news_agent import run as run_news

        results.append(run_news(dry_run=args.dry_run))

    if args.agent in ("research", "all"):
        from agents.research_agent import run as run_research

        results.append(run_research(dry_run=args.dry_run))

    print(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    main()
