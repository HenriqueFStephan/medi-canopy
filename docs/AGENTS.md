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

## 🔧 AI AGENT (issue solver)

**Workflow:** `.github/workflows/cursor-issue-solver.yml`
**Diagram:** [docs/workflows/ai-agent.md](./workflows/ai-agent.md)
**Script:** `scripts/run_issue_solver_agents.py`

Triggered only when an issue is labeled `solve` (not on pull requests or a
schedule). The job also ignores PRs that receive the `solve` label, because
GitHub treats pull requests as issues. The cloud agent rates the change 1–5,
merges complexity 1–3 into the default branch, and opens a pull request only for
complexity 4–5. Research notes (`research` / `daily-cannabis`) are never
dispatched.

**Manual run:** Actions tab → 🔧 AI AGENT → `workflow_dispatch` (`dry_run=true` by default).

## 🔬 WEEKLY PAPER REPORT (GitHub Action)

**Workflow:** `.github/workflows/daily-cannabis-research.yml` (Mondays 06:30 UTC)
**Diagram:** [docs/workflows/weekly-paper-report.md](./workflows/weekly-paper-report.md)
**Script:** `scripts/run_daily_cannabis_research.py`
**Catalog:** `agents/data/discovered_papers.json`

Launches a Cursor cloud agent that searches for peer-reviewed literature on
medical cannabis, hemp fibre in fashion/textiles, hemp construction materials,
agronomy, and policy. Only papers published in the **past 31 days** are eligible.
DOIs/URLs already listed in the catalog are passed to the agent and filtered out
so they are not posted again. Newly accepted papers are appended to the catalog.

The workflow waits for the run, parses the agent's JSON reply, and opens a
GitHub issue titled `[RESEARCH] Daily Cannabis {YYYY-MM-DD}` labelled
`research` + `daily-cannabis`.

**Reliability filter** — a paper reaches the issue only if it is flagged peer-reviewed,
names a journal, is not a preprint/blog/thesis/patent, has a valid DOI or a link on a
recognised publisher domain, reports a `published` date within 31 days, is not already
in the catalog, and reports confidence at or above `--min-confidence`
(default `0.7`). Discarded candidates are reduced to a count in the issue; their
details stay in the job summary and the uploaded artifact.

When nothing clears the filter, **no issue is created** — an empty digest is noise.

The 🔧 AI AGENT workflow only launches on the `solve` label, so research digests
are never dispatched as coding tasks.

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
