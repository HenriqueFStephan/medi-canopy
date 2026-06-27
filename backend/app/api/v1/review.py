"""Review queue API — agent discoveries awaiting author approval."""

from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.models.schemas import BlogPost, ReviewDecision, ReviewItem, ReviewStatus
from app.repositories.json_store import (
    blog_store,
    get_review_queue,
    new_id,
    news_store,
    save_review_queue,
)
from app.services.paper_normalizer import ScientificPaperNormalizer

router = APIRouter(prefix="/review", tags=["review"])
normalizer = ScientificPaperNormalizer()


@router.get("", response_model=list[ReviewItem])
def list_pending(status: str = "pending") -> list[ReviewItem]:
    items = get_review_queue()
    filtered = [i for i in items if i.get("status") == status]
    return [ReviewItem.model_validate(i) for i in filtered]


@router.get("/{item_id}", response_model=ReviewItem)
def get_item(item_id: str) -> ReviewItem:
    for item in get_review_queue():
        if item["id"] == item_id:
            return ReviewItem.model_validate(item)
    raise HTTPException(status_code=404, detail="Review item not found")


@router.post("/{item_id}/decide")
def decide(item_id: str, decision: ReviewDecision) -> dict:
    """
    Approve or reject a review item.

    On approve:
    - news → promoted to news_store
    - research → normalized to blog post via PaperNormalizer
    """
    queue = get_review_queue()
    target = None
    for item in queue:
        if item["id"] == item_id:
            target = item
            break
    if not target:
        raise HTTPException(status_code=404, detail="Review item not found")

    now = datetime.utcnow().isoformat()

    if decision.action == "reject":
        target["status"] = ReviewStatus.REJECTED.value
        target["decided_at"] = now
        target["notes"] = decision.notes
        save_review_queue(queue)
        return {"status": "rejected", "id": item_id}

    # Approve flow
    target["status"] = ReviewStatus.APPROVED.value
    target["decided_at"] = now
    payload = target.get("payload", {})
    item_type = target.get("item_type")

    if item_type == "news":
        record = {
            "id": new_id(),
            "status": ReviewStatus.APPROVED.value,
            "created_at": now,
            "published_at": now,
            **payload,
        }
        news_store.append(record)
    elif item_type == "research":
        normalized = normalizer.normalize(payload)
        blog_draft = normalizer.to_blog_post(normalized)
        record = {
            "id": new_id(),
            "author_name": "Papi Ro Ebers",
            "published_at": now,
            "updated_at": now,
            **blog_draft.model_dump(mode="json"),
        }
        blog_store.append(record)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown item_type: {item_type}")

    save_review_queue(queue)
    return {"status": "approved", "id": item_id, "published_type": item_type}
