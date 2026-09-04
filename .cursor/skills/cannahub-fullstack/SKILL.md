---
name: cannahub-fullstack
description: >-
  Implements features in Medi Canopy following Angular + FastAPI conventions.
  Use when adding API endpoints, frontend pages, or cross-stack features.
---

# Medi Canopy Full-Stack Development

## Backend (FastAPI)

1. Add schema in `backend/app/models/schemas.py`
2. Add router in `backend/app/api/v1/{module}.py`
3. Register in `backend/app/main.py`
4. Seed data in `backend/data/seed/` if needed

## Frontend (Angular 16)

1. Add interface in `frontend/src/app/core/models.ts`
2. Add API method in `frontend/src/app/core/api.service.ts`
3. Create standalone component in `frontend/src/app/features/`
4. Add lazy route in `frontend/src/app/app.routes.ts`
5. Use brand SCSS variables from `frontend/src/styles/_variables.scss`

## Agents

- Never publish without review
- Placeholder LLM: `LLM_PROVIDER=placeholder`
- Credentials: `debt.txt`

## Documentation

Update `docs/AGENT_NAVIGATION.md` when adding major modules.
