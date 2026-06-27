# Agent Navigation Map — CanaHub

**Purpose:** Help Cursor agents and developers find the right files quickly.

## "I need to…"

| Task | Go to |
|------|-------|
| Change brand colors | `frontend/src/styles/_variables.scss`, `docs/BRAND.md` |
| Add API endpoint | `backend/app/api/v1/`, register in `backend/app/main.py` |
| Modify news list UI | `frontend/src/app/features/news/` |
| Run news agent manually | `python -m agents.run --agent news` or `.cursor/skills/run-news-agent/` |
| Run research agent | `python -m agents.run --agent research` |
| Paper → blog formatting | `backend/app/services/paper_normalizer.py` |
| Add course placeholder | `backend/data/seed/courses.json`, `frontend/.../courses/` |
| Contact form | `frontend/.../contact/`, `backend/app/api/v1/contact.py` |
| Credentials / keys | `debt.txt` (local only), `backend/app/core/config.py` |
| Agent fixtures (no API) | `agents/fixtures/` |
| Cursor skills | `.cursor/skills/` |
| Cursor hooks | `.cursor/hooks.json`, `.cursor/hooks/` |
| MCP design | `.cursor/mcp/README.md` |
| Instagram link | `frontend/src/app/shared/footer/`, header social links |
| Seed blog from IG | `backend/data/seed/instagram_posts.json` |

## Module Dependency Graph

```
frontend/features/*  →  core/services/api.service.ts  →  backend /api/v1/*
backend/api/v1/*     →  services/*  →  repositories/*
agents/*             →  backend/app/agents/adapter.py  →  review queue files
```

## Do NOT

- Commit `debt.txt` with real passwords (gitignored)
- Publish `pending` review items to public API
- Edit `node_modules/` or `.venv/`

## Entry Points

| Component | Entry file |
|-----------|------------|
| Backend | `backend/app/main.py` |
| Frontend | `frontend/src/main.ts` |
| Agents CLI | `agents/run.py` |
| FastAPI OpenAPI | http://localhost:8000/docs |

## Test Commands

```bash
cd backend && pytest
cd frontend && npm test
python -m agents.run --agent news --dry-run
```
