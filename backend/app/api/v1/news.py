"""News articles API — published content and agent review integration."""

from datetime import datetime

from fastapi import APIRouter, HTTPException, Query

from app.core.locale import localize_item, localize_list, normalize_lang
from app.models.schemas import NewsArticle, NewsArticleCreate, ReviewStatus
from app.repositories.json_store import new_id, news_store

router = APIRouter(prefix="/news", tags=["news"])


@router.get("", response_model=list[NewsArticle])
def list_news(
    region: str | None = None,
    limit: int = 50,
    lang: str | None = Query(default=None),
) -> list[NewsArticle]:
    """Return published news articles, optionally filtered by region (BR, global)."""
    items = news_store.read_all()
    published = [i for i in items if i.get("status", "approved") == ReviewStatus.APPROVED.value]
    if region:
        published = [i for i in published if i.get("region") == region]
    published.sort(key=lambda x: x.get("published_at", ""), reverse=True)
    localized = localize_list(published[:limit], normalize_lang(lang))
    return [NewsArticle.model_validate(i) for i in localized]


@router.get("/{article_id}", response_model=NewsArticle)
def get_news(article_id: str, lang: str | None = Query(default=None)) -> NewsArticle:
    locale = normalize_lang(lang)
    for item in news_store.read_all():
        if item["id"] == article_id:
            return NewsArticle.model_validate(localize_item(item, locale))
    raise HTTPException(status_code=404, detail="Article not found")


@router.post("", response_model=NewsArticle, status_code=201)
def create_news(payload: NewsArticleCreate) -> NewsArticle:
    """Create news article (admin/manual — future: auth required)."""
    now = datetime.utcnow().isoformat()
    record = {
        "id": new_id(),
        "status": ReviewStatus.APPROVED.value,
        "created_at": now,
        "published_at": payload.published_at.isoformat() if payload.published_at else now,
        **payload.model_dump(mode="json"),
    }
    news_store.append(record)
    return NewsArticle.model_validate(record)
