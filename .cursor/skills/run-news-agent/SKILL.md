---
name: run-news-agent
description: >-
  Runs the Medi Canopy daily news agent manually, debugs output, and explains review
  queue flow. Use when triggering news search, testing agents, or DevOps scheduling.
---

# Run News Agent

## Manual execution

From repository root:

```bash
python -m agents.run --agent news
python -m agents.run --agent news --dry-run
```

Windows:

```powershell
.\scripts\run-agents.ps1 -Agent news
```

## What it does

1. Loads `agents/config/news_sources.yaml`
2. Calls `agents/llm_client.py` (placeholder → `agents/fixtures/news_sample.json`)
3. Enqueues items to `backend/data/review_queue.json` via `app.agents.adapter`
4. Logs run to `agents/output/YYYY-MM-DD_news.json`

## Activating real LLM

Set in `debt.txt` / `.env`:

- `LLM_PROVIDER=openai`
- `OPENAI_API_KEY=sk-...`

Then implement web search in `agents/llm_client.py::search_news`.

## Approve for publish

```http
POST /api/v1/review/{id}/decide
{"action": "approve"}
```

## Key files

- `agents/news_agent.py`
- `backend/app/api/v1/review.py`
- `docs/AGENTS.md`
