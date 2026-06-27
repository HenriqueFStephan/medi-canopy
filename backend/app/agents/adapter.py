"""
Bridge between standalone agent runners and the backend review queue.

Agents write pending items here; author approves via /api/v1/review/{id}/decide.
"""

from datetime import datetime, timezone

from app.repositories.json_store import get_review_queue, new_id, save_review_queue


def enqueue_review_item(
    item_type: str,
    title: str,
    payload: dict,
    source_agent: str,
) -> dict:
    """Add a pending item to the review queue."""
    item = {
        "id": new_id(),
        "item_type": item_type,
        "status": "pending",
        "title": title,
        "payload": payload,
        "discovered_at": datetime.now(timezone.utc).isoformat(),
        "source_agent": source_agent,
    }
    queue = get_review_queue()
    queue.append(item)
    save_review_queue(queue)
    return item
