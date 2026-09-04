---
name: run-research-agent
description: >-
  Runs the Medi Canopy research agent for scientific papers, email digest placeholders,
  and PaperNormalizer blog conversion. Use for scholarly content pipeline work.
---

# Run Research Agent

## Manual execution

```bash
python -m agents.run --agent research
python -m agents.run --agent research --dry-run
```

## Pipeline

1. `agents/research_agent.py` fetches papers (fixture or API)
2. `ScientificPaperNormalizer` in `backend/app/services/paper_normalizer.py`
3. Email digest → `agents/output/YYYY-MM-DD_research_email.html` (SMTP placeholder)
4. Review queue → author approves → auto blog post

## Paper → Blog

```python
from app.services.paper_normalizer import ScientificPaperNormalizer
normalizer = ScientificPaperNormalizer()
norm = normalizer.normalize(raw_dict)
blog = normalizer.to_blog_post(norm)
```

## APIs needed

See `docs/RESOURCES_NEEDED.md` — Semantic Scholar, PubMed, OpenAlex.

## Key files

- `agents/research_agent.py`
- `agents/templates/research_digest.html`
- `backend/app/services/paper_normalizer.py`
