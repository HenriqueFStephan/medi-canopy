# Implementation Plan — Phase 1 Demo

## Completed in this deliverable

- [x] Monorepo structure (frontend + backend + agents)
- [x] Brand identity & SCSS tokens
- [x] FastAPI modular API with seed data
- [x] Angular SPA with News, Blog, Courses, Services, Contact, Home
- [x] News & Research agent placeholders + manual CLI
- [x] PaperNormalizer for blog-ready research posts
- [x] Review queue architecture (pending → approved)
- [x] Instagram link + seed blog posts from @papiroebers style content
- [x] Cursor skills, hooks, agents, MCP design docs
- [x] debt.txt credential template
- [x] Documentation suite

## Phase 2 — Author workflow

- [ ] Admin auth (JWT)
- [ ] Review dashboard UI
- [ ] Rich text editor for blog
- [ ] Approve/reject review items from frontend

## Phase 3 — Live agents

- [ ] Wire OpenAI/Anthropic in `agents/llm_client.py`
- [ ] Semantic Scholar / PubMed clients
- [ ] SMTP email sending for research digest
- [ ] Cron / GitHub Actions schedule

## Phase 4 — Courses & commerce

- [ ] Course enrollment model
- [ ] Payment placeholder (Stripe/Mercado Pago)
- [ ] Video hosting integration

## Phase 5 — Scale

- [ ] PostgreSQL + Alembic
- [ ] Redis job queue
- [ ] Full-text search
- [x] i18n (PT-BR primary, EN secondary)

## Estimated effort (rough)

| Phase | Duration |
|-------|----------|
| 1 Demo | Done |
| 2 Author workflow | 2–3 weeks |
| 3 Live agents | 1–2 weeks |
| 4 Courses | 2–4 weeks |
| 5 Scale | Ongoing |
