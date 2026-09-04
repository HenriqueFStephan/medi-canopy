---
name: project-navigation
description: >-
  Navigates the Medi Canopy monorepo (Angular frontend, FastAPI backend, agents).
  Use when exploring medi-canopy, finding modules, or understanding architecture.
---

# Medi Canopy Project Navigation

## Layout

| Path | Role |
|------|------|
| `frontend/` | Angular 16 SPA |
| `backend/app/` | FastAPI API |
| `agents/` | News & research agent runners |
| `docs/` | Architecture, brand, agent docs |
| `.cursor/` | Skills, hooks, agent definitions, MCP design |
| `debt.txt` | Credential placeholders (gitignored) |

## Quick commands

```bash
# Backend
cd backend && uvicorn app.main:app --reload

# Frontend
cd frontend && npm start

# Agents
python -m agents.run --agent news
python -m agents.run --agent research
```

## Full map

Read [docs/AGENT_NAVIGATION.md](../../docs/AGENT_NAVIGATION.md) for task → file routing.

## Conventions

- API prefix: `/api/v1`
- Agent output never auto-publishes — review queue first
- Brand tokens: `docs/BRAND.md`, `frontend/src/styles/_variables.scss`
