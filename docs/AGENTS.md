# Agent System — Medi Canopy

## Overview

Two primary agents support content discovery. Neither publishes automatically.

| Agent | Schedule | Output | Manual run |
|-------|----------|--------|------------|
| **News** | Daily 06:00 (configurable) | Review queue JSON + API `pending` items | `python -m agents.run --agent news` |
| **Research** | Daily 07:00 | Email digest + review queue papers | `python -m agents.run --agent research` |

## Placeholder Mode

When `LLM_PROVIDER=placeholder` (see `debt.txt`), agents use mock data from:

- `agents/fixtures/news_sample.json`
- `agents/fixtures/papers_sample.json`

This allows full pipeline testing without API keys.

## News Agent

**Module:** `agents/news_agent.py`

**Search domains:**

- Brazil cannabis policy & ANVISA
- Medical studies & clinical trials
- International market & regulation
- Industrial hemp & textiles
- Cultivation technology

**Pipeline:**

```
load_config → search_sources (LLM/tool) → normalize → dedupe → save_review_queue → log
```

**Config:** `agents/config/news_sources.yaml`

## Research Agent

**Module:** `agents/research_agent.py`

**Pipeline:**

```
query scholarly APIs (placeholder) → PaperNormalizer → email digest → save_review_queue
```

**Email template:** `agents/templates/research_digest.html`

Author reviews email and approves via future admin UI or API `POST /api/v1/review/{id}/approve`.

## Scientific Paper → Blog

On approval, `PaperNormalizer.to_blog_post()` produces:

```python
{
  "title": "...",
  "slug": "...",
  "excerpt": "...",
  "content_markdown": "...",
  "tags": [...],
  "source_type": "research",
  "citation": "..."
}
```

## Cursor Integration

| Asset | Path | Purpose |
|-------|------|---------|
| Skill: run-news-agent | `.cursor/skills/run-news-agent/` | How to trigger & debug news agent |
| Skill: run-research-agent | `.cursor/skills/run-research-agent/` | Research agent & paper flow |
| Skill: project-navigation | `.cursor/skills/project-navigation/` | Repo map for agents |
| Agent: content-reviewer | `.cursor/agents/content-reviewer.md` | Review queue workflows |
| Agent: full-stack-dev | `.cursor/agents/full-stack-dev.md` | Angular + FastAPI conventions |
| Hooks | `.cursor/hooks.json` | Protect secrets, format Python |
| MCP design | `.cursor/mcp/README.md` | Future MCP servers for news/research |

## Daily Cannabis Research (GitHub Action)

**Workflow:** `.github/workflows/daily-cannabis-research.yml` (daily 06:30 UTC)
**Script:** `scripts/run_daily_cannabis_research.py`

Launches a Cursor cloud agent that searches for recent peer-reviewed literature on
medical cannabis, hemp fibre in fashion/textiles, hemp construction materials,
agronomy, and policy. The workflow waits for the run, parses the agent's JSON reply,
and opens a GitHub issue titled `Daily Cannabis {YYYY-MM-DD}` with the surviving links.

**Reliability filter** — a paper reaches the issue only if it is flagged peer-reviewed,
names a journal, is not a preprint/blog/thesis/patent, has a valid DOI or a link on a
recognised publisher domain, and reports confidence at or above `--min-confidence`
(default `0.7`). Discarded candidates are reduced to a count in the issue; their
details stay in the job summary and the uploaded artifact.

When nothing clears the filter, **no issue is created** — an empty digest is noise.

Issues are labelled `daily-cannabis`, which `run_issue_solver_agents.py` excludes from
dispatch so the issue solver never tries to "fix" a research digest.

**Manual run:**

```bash
python scripts/run_daily_cannabis_research.py \
  --repo owner/repo --repo-url https://github.com/owner/repo --dry-run
```

## DevOps Scheduling (future)

**GitHub Actions example** (`.github/workflows/agents-daily.yml` — placeholder):

```yaml
schedule:
  - cron: '0 9 * * *'  # UTC
```

**Windows Task Scheduler:** use `scripts/run-agents.ps1 -Agent news`

## Logs

Agent runs write to `agents/output/YYYY-MM-DD_{agent}.json`.
