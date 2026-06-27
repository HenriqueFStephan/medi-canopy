# MCP Server Design — CanaHub (Placeholders)

MCP servers are **designed but not implemented**. Use this document when wiring Cursor MCP tools in a future phase.

## Planned servers

### 1. cannahub-news-mcp

**Purpose:** Expose news search tools to Cursor agents.

| Tool | Description |
|------|-------------|
| `search_news` | Query by topic/region |
| `list_review_queue` | Pending news items |
| `approve_news` | Promote to published |

**Config placeholder** (`debt.txt`):

```
MCP_NEWS_SERVER=placeholder://localhost:3100
```

**Future package:** `mcp-servers/news/` (not created in demo)

### 2. cannahub-research-mcp

**Purpose:** Scholarly API wrappers for research agent.

| Tool | Description |
|------|-------------|
| `search_papers` | PubMed/OpenAlex query |
| `normalize_paper` | Run PaperNormalizer |
| `send_digest` | Trigger email placeholder |

**Config placeholder:**

```
MCP_RESEARCH_SERVER=placeholder://localhost:3101
```

## Example mcp.json (future)

```json
{
  "mcpServers": {
    "cannahub-news": {
      "command": "python",
      "args": ["-m", "mcp_servers.news"],
      "env": {
        "OPENAI_API_KEY": "${OPENAI_API_KEY}"
      }
    }
  }
}
```

## Current alternative

Use project skills instead:

- `.cursor/skills/run-news-agent/`
- `.cursor/skills/run-research-agent/`

And CLI: `python -m agents.run --agent {news|research}`
