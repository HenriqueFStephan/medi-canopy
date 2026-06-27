"""
Daily Research Agent — fetches scientific papers and emails digest to author.

Papers are normalized and queued for review; email is placeholder until SMTP configured.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from app.agents.adapter import enqueue_review_item  # noqa: E402
from app.services.paper_normalizer import ScientificPaperNormalizer  # noqa: E402
from agents.llm_client import LLMClient  # noqa: E402

AGENTS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = AGENTS_DIR / "output"
TEMPLATES_DIR = AGENTS_DIR / "templates"


def load_config() -> dict:
    return yaml.safe_load(
        (AGENTS_DIR / "config" / "research_sources.yaml").read_text(encoding="utf-8")
    )


def send_email_digest(papers: list[dict], *, dry_run: bool) -> dict:
    """
    PLACEHOLDER: writes digest to agents/output/ instead of SMTP.

    Activate with SMTP_* keys in debt.txt — see docs/RESOURCES_NEEDED.md.
    """
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    digest_path = OUTPUT_DIR / f"{date_str}_research_email.html"

    template = (TEMPLATES_DIR / "research_digest.html").read_text(encoding="utf-8")
    rows = ""
    for p in papers:
        rows += f"<li><strong>{p.get('title')}</strong> — {p.get('journal', 'N/A')}</li>\n"

    html = template.replace("{{DATE}}", date_str).replace("{{PAPER_LIST}}", rows)
    digest_path.write_text(html, encoding="utf-8")

    return {
        "sent": False,
        "placeholder_file": str(digest_path),
        "message": "SMTP not configured — digest saved to file",
    }


def run(*, dry_run: bool = False) -> dict:
    config = load_config()
    client = LLMClient()
    normalizer = ScientificPaperNormalizer()

    raw_papers = client.fetch_papers(config.get("queries", []))
    normalized = [normalizer.normalize(p).model_dump() for p in raw_papers]
    enqueued = []

    for raw, norm in zip(raw_papers, normalized):
        if dry_run:
            enqueued.append(norm)
            continue
        review = enqueue_review_item(
            item_type="research",
            title=norm["title"],
            payload=raw,
            source_agent="research_agent",
        )
        enqueued.append(review)

    email_result = send_email_digest(normalized, dry_run=dry_run)

    result = {
        "agent": "research",
        "run_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": dry_run,
        "count": len(enqueued),
        "email": email_result,
        "items": enqueued,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    (OUTPUT_DIR / f"{date_str}_research.json").write_text(
        json.dumps(result, indent=2, default=str), encoding="utf-8"
    )
    return result


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    summary = run(dry_run=dry)
    print(json.dumps(summary, indent=2, default=str))
