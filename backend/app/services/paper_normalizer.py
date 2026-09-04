"""
ScientificPaperNormalizer — converts raw scholarly data into blog-ready content.

Used by the research agent pipeline and the review approval flow so the author
can publish approved papers with consistent formatting.
"""

import re
import unicodedata
from typing import Any

from app.models.schemas import (
    BlogPostCreate,
    ContentSource,
    ScientificPaperNormalized,
    ScientificPaperRaw,
)


def _slugify(text: str, max_length: int = 80) -> str:
    """Generate URL-safe slug from title."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[-\s]+", "-", text).strip("-")
    return text[:max_length].rstrip("-")


def _infer_tags(paper: ScientificPaperRaw) -> list[str]:
    """Infer topical tags from keywords and abstract (placeholder heuristics)."""
    blob = " ".join(paper.keywords + [paper.abstract, paper.title]).lower()
    tag_map = {
        "medical": ["clinical", "patient", "cbd", "thc", "therapeutic", "medical"],
        "policy": ["regulation", "legal", "anvisa", "legislation", "policy"],
        "cultivation": ["grow", "cultivation", "harvest", "greenhouse", "indoor"],
        "textile": ["hemp", "fiber", "textile", "industrial"],
        "brazil": ["brazil", "brasil", "brazilian"],
    }
    tags: list[str] = []
    for tag, keywords in tag_map.items():
        if any(kw in blob for kw in keywords):
            tags.append(tag)
    if not tags:
        tags.append("research")
    return tags


def _build_citation(paper: ScientificPaperRaw) -> str:
    """APA-style citation block (simplified)."""
    authors = ", ".join(paper.authors[:3])
    if len(paper.authors) > 3:
        authors += ", et al."
    year = (paper.published_date or "")[:4] or "n.d."
    journal = paper.journal or "Preprint"
    doi_part = f" https://doi.org/{paper.doi}" if paper.doi else ""
    return f"{authors} ({year}). {paper.title}. *{journal}.*{doi_part}"


class ScientificPaperNormalizer:
    """
    Normalizes raw scientific paper records for author review and blog publishing.

    Example:
        normalizer = ScientificPaperNormalizer()
        normalized = normalizer.normalize(raw_paper)
        blog_draft = normalizer.to_blog_post(normalized)
    """

    def normalize(self, raw: ScientificPaperRaw | dict[str, Any]) -> ScientificPaperNormalized:
        """Convert raw API/agent payload to normalized review structure."""
        if isinstance(raw, dict):
            raw = ScientificPaperRaw.model_validate(raw)

        tags = _infer_tags(raw)
        citation = _build_citation(raw)

        return ScientificPaperNormalized(
            title=raw.title,
            slug=_slugify(raw.title),
            authors=raw.authors,
            abstract=raw.abstract,
            summary_pt=self._placeholder_summary(raw),
            doi=raw.doi,
            journal=raw.journal,
            published_date=raw.published_date,
            url=raw.url,
            tags=tags,
            citation_block=citation,
            hero_image_url=None,
        )

    def to_blog_post(self, paper: ScientificPaperNormalized) -> BlogPostCreate:
        """
        Build a BlogPostCreate from an approved normalized paper.

        Content markdown includes abstract, placeholder summary, and citation.
        """
        authors_line = ", ".join(paper.authors) if paper.authors else "Autores não informados"
        summary_section = (
            f"## Resumo\n\n{paper.summary_pt}\n\n"
            if paper.summary_pt
            else "## Resumo\n\n*Resumo em português pendente — ativar LLM em produção.*\n\n"
        )

        content = f"""# {paper.title}

**Publicado em:** {paper.published_date or "Data não informada"}  
**Autores:** {authors_line}  
**Fonte:** {paper.journal or "Periódico não informado"}

{summary_section}

## Abstract

{paper.abstract}

## Referência

{paper.citation_block}

---
*Artigo científico curado para o blog Medi Canopy. Consulte a fonte original antes de decisões clínicas ou regulatórias.*
"""

        excerpt = paper.summary_pt or (paper.abstract[:280] + "…" if len(paper.abstract) > 280 else paper.abstract)

        return BlogPostCreate(
            title=paper.title,
            slug=paper.slug,
            excerpt=excerpt,
            content_markdown=content,
            tags=paper.tags,
            source_type=ContentSource.AGENT_RESEARCH,
            cover_image_url=paper.hero_image_url,
            citation=paper.citation_block,
        )

    def _placeholder_summary(self, raw: ScientificPaperRaw) -> str:
        """
        Placeholder PT summary until LLM integration is active.

        When LLM_PROVIDER != placeholder, replace with llm_client.summarize_pt(raw).
        """
        if not raw.abstract:
            return ""
        # First two sentences as demo stand-in
        sentences = re.split(r"(?<=[.!?])\s+", raw.abstract.strip())
        return " ".join(sentences[:2])
