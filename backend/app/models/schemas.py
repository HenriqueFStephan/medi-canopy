"""
Shared Pydantic schemas for Medi Canopy API requests and responses.

All public API contracts are defined here for consistency between
frontend TypeScript interfaces and backend validation.
"""

import re
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl, field_validator

# CSS .feature-list already renders 01, 02, … — strip the same index from titles.
_SERVICE_TITLE_INDEX = re.compile(r"^\s*\d+\s*[—–−-]\s*")


class ReviewStatus(str, Enum):
    """Lifecycle state for agent-discovered content awaiting author approval."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ContentSource(str, Enum):
    """Origin of a content item."""

    AGENT_NEWS = "agent_news"
    AGENT_RESEARCH = "agent_research"
    MANUAL = "manual"
    INSTAGRAM = "instagram"


# --- News ---


class NewsArticleBase(BaseModel):
    title: str
    summary: str
    content: str = ""
    source_url: Optional[str] = None
    source_name: Optional[str] = None
    region: str = "BR"
    tags: list[str] = Field(default_factory=list)
    published_at: Optional[datetime] = None


class NewsArticle(NewsArticleBase):
    id: str
    status: ReviewStatus = ReviewStatus.APPROVED
    created_at: datetime


class NewsArticleCreate(NewsArticleBase):
    pass


# --- Blog ---


class BlogPostBase(BaseModel):
    title: str
    slug: str
    excerpt: str
    content_markdown: str
    tags: list[str] = Field(default_factory=list)
    source_type: ContentSource = ContentSource.MANUAL
    cover_image_url: Optional[str] = None
    instagram_url: Optional[str] = None
    citation: Optional[str] = None


class BlogPost(BlogPostBase):
    id: str
    author_name: str = "Papi Ro Ebers"
    published_at: datetime
    updated_at: Optional[datetime] = None


class BlogPostCreate(BlogPostBase):
    pass


# --- Scientific papers (research agent) ---


class ScientificPaperRaw(BaseModel):
    """Raw paper payload from scholarly APIs or agent fixtures."""

    title: str
    authors: list[str] = Field(default_factory=list)
    abstract: str = ""
    doi: Optional[str] = None
    journal: Optional[str] = None
    published_date: Optional[str] = None
    url: Optional[str] = None
    keywords: list[str] = Field(default_factory=list)


class ScientificPaperNormalized(BaseModel):
    """Normalized paper ready for author review or blog conversion."""

    title: str
    slug: str
    authors: list[str]
    abstract: str
    summary_pt: str = ""
    doi: Optional[str] = None
    journal: Optional[str] = None
    published_date: Optional[str] = None
    url: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    citation_block: str = ""
    hero_image_url: Optional[str] = None


# --- Review queue ---


class ReviewItem(BaseModel):
    id: str
    item_type: str  # "news" | "research"
    status: ReviewStatus = ReviewStatus.PENDING
    title: str
    payload: dict
    discovered_at: datetime
    source_agent: str


class ReviewDecision(BaseModel):
    action: str = Field(..., pattern="^(approve|reject)$")
    notes: Optional[str] = None


# --- Courses ---


class CourseModule(BaseModel):
    title: str
    description: str
    duration_minutes: int = 0


class Course(BaseModel):
    id: str
    title: str
    slug: str
    description: str
    level: str = "intermediário"
    price_display: str = "Em breve"
    cover_image_url: Optional[str] = None
    modules: list[CourseModule] = Field(default_factory=list)
    published: bool = True
    coming_soon: bool = True


# --- Services (consulting showcase) ---


class ServiceOffering(BaseModel):
    id: str
    title: str
    description: str
    icon: str = "leaf"
    highlights: list[str] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def strip_list_index(cls, value: str) -> str:
        return _SERVICE_TITLE_INDEX.sub("", value).strip()


# --- Contact ---


class ContactMessageCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    subject: str = Field(..., min_length=3, max_length=200)
    message: str = Field(..., min_length=10, max_length=5000)


class ContactMessageResponse(BaseModel):
    success: bool
    message: str


class ConsultingRequestCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    company: str = Field("", max_length=160)
    phone: str = Field("", max_length=40)
    service_ids: list[str] = Field(default_factory=list, max_length=20)
    message: str = Field(..., min_length=10, max_length=5000)

    @field_validator("name", "company", "phone", "message")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()

    @field_validator("service_ids")
    @classmethod
    def unique_service_ids(cls, value: list[str]) -> list[str]:
        seen: list[str] = []
        for item in value:
            cleaned = item.strip()
            if cleaned and cleaned not in seen:
                seen.append(cleaned)
        return seen


class ConsultingRequestResponse(BaseModel):
    success: bool
    message: str
    email_sent: bool = False


# --- Health ---


class HealthResponse(BaseModel):
    status: str
    version: str = "0.1.0"
    environment: str
