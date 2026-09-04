# Deliverable Report — Medi Canopy Phase 1 Demo

**Date:** 2026-06-27  
**Project:** Site_Biel — Cannabis Information Hub

---

## Executive Summary

A full monorepo demo was created with:

- **Angular 16** frontend (News, Blog, Courses, Services, Contact, Home)
- **FastAPI** backend with versioned REST API
- **Python agents** for daily news and research (placeholder LLM, manual CLI)
- **Cursor agent tooling** (skills, hooks, agent defs, MCP design)
- **Brand identity** and documentation suite

Official name: **Medi Canopy**.

---

## What Was Built

### Frontend (`frontend/`)

| Route | Feature |
|-------|---------|
| `/` | Hero, feature grid, CTA |
| `/news` | Filterable news (BR / global) |
| `/blog` | Post list + detail with markdown |
| `/courses` | Course templates, "Em breve" |
| `/services` | Consulting showcase (4 offerings) |
| `/contact` | Reactive form → API |

Instagram [@papiroebers](https://www.instagram.com/papiroebers) linked in header, footer, home, blog.

Design inspired by [4trees](https://4treesbuilding.ca/projects) and [PlantManager](https://plantmanager.com.br/).

### Backend (`backend/`)

- `GET/POST /api/v1/news`
- `GET/POST /api/v1/blog`
- `GET /api/v1/courses`
- `GET /api/v1/services`
- `POST /api/v1/contact`
- `GET/POST /api/v1/review` — approval workflow

**ScientificPaperNormalizer** converts approved papers to blog markdown.

### Agents (`agents/`)

| Agent | Schedule (planned) | Manual command |
|-------|-------------------|----------------|
| News | Daily 06:00 | `python -m agents.run --agent news` |
| Research | Daily 07:00 | `python -m agents.run --agent research` |

Output: `agents/output/` + `backend/data/review_queue.json`

### Cursor Tooling (`.cursor/`)

| Asset | Path |
|-------|------|
| Skills | `skills/project-navigation`, `run-news-agent`, `run-research-agent`, `cannahub-fullstack` |
| Hooks | `hooks.json` + secret check + doc reminder |
| Agents | `agents/content-reviewer.md`, `full-stack-dev.md` |
| Rules | `rules/cannahub.mdc` |
| MCP design | `mcp/README.md` (placeholders only) |

### Documentation (`docs/`)

- ARCHITECTURE.md — system design + mermaid diagram
- BRAND.md — palette, typography, voice
- AGENTS.md — agent workflows
- DEVELOPMENT.md — dev setup
- RESOURCES_NEEDED.md — external APIs & keys
- AGENT_NAVIGATION.md — task → file map
- IMPLEMENTATION_PLAN.md — phases 2–5

### Credentials

`debt.txt` — all placeholder keys documented (gitignored).

---

## How to Run

```powershell
# Terminal 1 — Backend
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Terminal 2 — Frontend
cd frontend
npm install
npm start

# Terminal 3 — Test agent
python -m agents.run --agent all --dry-run
```

---

## Resources Needed (Action Items)

See **docs/RESOURCES_NEEDED.md** for full detail.

| Priority | Resource |
|----------|----------|
| High | LLM API key (OpenAI/Anthropic) |
| High | SMTP for research email digest |
| Medium | Semantic Scholar / PubMed keys |
| Low | Instagram Graph API for auto-sync |
| Later | PostgreSQL, Redis, hosting |

---

## Next Steps (Phase 2+)

1. Author admin UI for review queue
2. Wire real LLM + scholarly APIs
3. Rich text blog editor
4. Course enrollment & payments
5. Production deploy + LGPD privacy policy

---

## File Count Overview

- ~80+ files across frontend, backend, agents, docs, .cursor
- Seed content: 3 news, 3 blog (Instagram-style), 2 courses, 4 services
