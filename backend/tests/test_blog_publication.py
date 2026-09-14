"""Blog publication date display and sorting."""

from app.services.blog_publication import (
    normalize_publication_date,
    publication_sort_key,
    resolve_publication_date,
)


def test_normalize_publication_date_handles_partial_dates():
    assert normalize_publication_date("2025-10") == "2025-10-01"
    assert normalize_publication_date("2024") == "2024-01-01"
    assert normalize_publication_date("2025-06-23") == "2025-06-23"
    assert normalize_publication_date(None) is None


def test_resolve_publication_date_prefers_scholarly_date_for_research():
    item = {
        "source_type": "agent_research",
        "published_date": "2025-05-14",
        "published_at": "2026-09-07T12:02:00",
    }
    assert resolve_publication_date(item) == "2025-05-14"


def test_resolve_publication_date_falls_back_for_manual_posts():
    item = {
        "source_type": "manual",
        "published_at": "2026-03-01T10:00:00",
    }
    assert resolve_publication_date(item) == "2026-03-01"


def test_resolve_publication_date_missing_for_research_without_date():
    item = {
        "source_type": "agent_research",
        "published_at": "2026-09-07T12:02:00",
    }
    assert resolve_publication_date(item) is None


def test_publication_sort_key_orders_newest_first():
    items = [
        {"source_type": "agent_research", "published_date": "2024-01-01", "id": "old"},
        {"source_type": "agent_research", "published_date": "2026-08-31", "id": "new"},
        {"source_type": "agent_research", "published_at": "2026-09-07T12:00:00", "id": "undated"},
    ]
    ordered = sorted(items, key=publication_sort_key, reverse=True)
    assert [item["id"] for item in ordered] == ["new", "old", "undated"]


def test_list_blog_sorted_by_publication_date():
    from fastapi.testclient import TestClient

    from app.main import app

    api = TestClient(app)
    response = api.get("/api/v1/blog")
    assert response.status_code == 200
    rows = response.json()
    assert rows
    assert rows[0]["published_date"] == "2026-09-12"
    assert rows[0]["slug"] == (
        "a-randomized-four-period-cross-over-phase-i-study-to-assess-bioavailability-bioe"
    )

    dates = [row.get("published_date") for row in rows if row.get("published_date")]
    assert dates == sorted(dates, reverse=True)


ISSUE28_DOIS = [
    "10.1186/s12870-026-09909-5",
    "10.3389/fpls.2026.1930650",
    "10.1186/s42238-026-00485-x",
    "10.12912/27197050/231235",
    "10.3390/f17091068",
    "10.1038/s41386-026-02533-9",
    "10.1007/s40261-026-01595-3",
    "10.1186/s42238-026-00492-y",
    "10.1208/s12248-026-01281-4",
    "10.1186/s42238-026-00487-9",
    "10.3390/fib14090095",
    "10.1016/j.clcb.2026.100232",
]


def test_issue28_research_posts_are_published():
    from fastapi.testclient import TestClient

    from app.main import app
    from app.repositories.json_store import blog_store

    api = TestClient(app)
    response = api.get("/api/v1/blog")
    assert response.status_code == 200
    rows = response.json()
    citations = " ".join(row.get("citation") or "" for row in rows)
    for doi in ISSUE28_DOIS:
        assert doi in citations

    seed_rows = blog_store.read_all()
    issue28_rows = [
        row
        for row in seed_rows
        if row.get("id", "").startswith("blog-research-20260914-")
    ]
    assert len(issue28_rows) == 12
    for row in issue28_rows:
        assert row.get("source_type") == "agent_research"
        assert row.get("title_pt")
        assert row.get("i18n", {}).get("en", {}).get("excerpt")
        assert "## Por que importa" in row.get("content_markdown", "")


def test_to_blog_post_carries_published_date():
    from app.models.schemas import ScientificPaperRaw
    from app.services.paper_normalizer import ScientificPaperNormalizer

    normalizer = ScientificPaperNormalizer()
    raw = ScientificPaperRaw(
        title="Sample Paper",
        authors=["A. Author"],
        abstract="Abstract text.",
        published_date="2025-03-15",
    )
    blog = normalizer.to_blog_post(normalizer.normalize(raw))
    assert blog.published_date == "2025-03-15"
