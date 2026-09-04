"""
CanaHub FastAPI application entry point.

Run: uvicorn app.main:app --reload --port 8000
"""

from fastapi import FastAPI

from app.api.v1 import blog, contact, courses, news, review, services
from app.core.config import get_settings
from app.core.cors import configure_cors
from app.models.schemas import HealthResponse
from app.repositories.json_store import blog_store, courses_store, news_store, services_store

settings = get_settings()

app = FastAPI(
    title="CanaHub API",
    description="Cannabis information hub — news, blog, courses, services, contact.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

configure_cors(app)

API_PREFIX = "/api/v1"

app.include_router(news.router, prefix=API_PREFIX)
app.include_router(blog.router, prefix=API_PREFIX)
app.include_router(courses.router, prefix=API_PREFIX)
app.include_router(services.router, prefix=API_PREFIX)
app.include_router(contact.router, prefix=API_PREFIX)
app.include_router(review.router, prefix=API_PREFIX)


@app.get("/health", response_model=HealthResponse, tags=["health"])
def health() -> HealthResponse:
    return HealthResponse(status="ok", environment=settings.app_env)


@app.get("/", tags=["health"])
def root() -> dict:
    return {
        "name": "CanaHub API",
        "docs": "/docs",
        "instagram": settings.instagram_url,
    }


@app.post("/api/v1/admin/reseed", tags=["admin"], include_in_schema=False)
def reseed_demo_stores() -> dict:
    """Reload news/blog/courses/services from committed seed JSON (demo only)."""
    news_store.load_seed()
    blog_store.load_seed()
    courses_store.load_seed()
    services_store.load_seed()
    return {"status": "reseeded"}
