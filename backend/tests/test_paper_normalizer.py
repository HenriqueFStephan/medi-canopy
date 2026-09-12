"""Tests for ScientificPaperNormalizer."""

from app.models.schemas import ScientificPaperRaw
from app.services.paper_normalizer import ScientificPaperNormalizer


def test_normalize_creates_slug_and_tags():
    raw = ScientificPaperRaw(
        title="CBD for Epilepsy in Brazil",
        authors=["Silva, M."],
        abstract="Clinical trial of cannabidiol for epilepsy patients in Brazil.",
        doi="10.1000/test",
        journal="Test Journal",
        published_date="2026-01-01",
    )
    normalizer = ScientificPaperNormalizer()
    result = normalizer.normalize(raw)

    assert result.slug == "cbd-for-epilepsy-in-brazil"
    assert "medical" in result.tags or "brazil" in result.tags
    assert result.citation_block


def test_to_blog_post_keeps_portuguese_title():
    raw = ScientificPaperRaw(
        title="Hemp Textiles Review",
        title_pt="Revisão de têxteis de cânhamo",
        authors=["Weber, J."],
        abstract="Industrial hemp fibers in sustainable textiles.",
        journal="Textile Journal",
    )
    normalizer = ScientificPaperNormalizer()
    blog = normalizer.to_blog_post(normalizer.normalize(raw))
    assert blog.title == "Hemp Textiles Review"
    assert blog.title_pt == "Revisão de têxteis de cânhamo"


def test_to_blog_post_markdown():
    raw = ScientificPaperRaw(
        title="Hemp Textiles Review",
        authors=["Weber, J."],
        abstract="Industrial hemp fibers in sustainable textiles.",
        journal="Textile Journal",
    )
    normalizer = ScientificPaperNormalizer()
    norm = normalizer.normalize(raw)
    blog = normalizer.to_blog_post(norm)

    assert blog.slug == norm.slug
    assert "Hemp Textiles Review" in blog.content_markdown
    assert blog.source_type.value == "agent_research"


def test_to_blog_post_includes_markdown_source_link():
    raw = ScientificPaperRaw(
        title="CBD trial",
        authors=["Silva, M."],
        abstract="A trial.",
        doi="10.1000/test",
        journal="Test Journal",
        published_date="2026-01-01",
        url="https://doi.org/10.1000/test",
    )
    normalizer = ScientificPaperNormalizer()
    blog = normalizer.to_blog_post(normalizer.normalize(raw))
    assert "[Test Journal](https://doi.org/10.1000/test)" in blog.content_markdown
    assert "[10.1000/test](https://doi.org/10.1000/test)" in (blog.citation or "")
