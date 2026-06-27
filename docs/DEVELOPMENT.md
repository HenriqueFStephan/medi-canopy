# Development Guide

## Prerequisites

- Node.js 16+ (18+ recommended for latest Angular)
- Python 3.11+
- npm 8+

## Repository Layout

See [ARCHITECTURE.md](./ARCHITECTURE.md).

## Backend Conventions

- **Framework:** FastAPI
- **Style:** Black-compatible, type hints required
- **Modules:** One router per domain under `app/api/v1/`
- **Schemas:** Pydantic v2 in `app/models/schemas.py`
- **Tests:** `backend/tests/` (pytest)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend Conventions

- **Framework:** Angular 16 standalone components
- **Style:** SCSS with brand variables
- **API:** `environment.apiUrl` → backend
- **Lazy routes** per feature module

```bash
cd frontend
npm install
npm start
```

## Environment

Copy keys from `debt.txt` into `backend/.env` (gitignored). Never commit secrets.

## Adding a News Source

1. Edit `agents/config/news_sources.yaml`
2. Update `agents/news_agent.py` search prompt if needed
3. Run manual agent and verify `agents/output/`

## Adding a Blog Post Manually

`POST /api/v1/blog` with JSON body (see OpenAPI docs) or seed via `backend/data/seed/blog.json`.

## Code Documentation

- Python: module docstrings + Google-style on public functions
- TypeScript: JSDoc on services and public component APIs

## Git Workflow

- `main` — stable demo
- Feature branches per module
- Conventional commits: `feat(blog):`, `fix(api):`, `docs:`
