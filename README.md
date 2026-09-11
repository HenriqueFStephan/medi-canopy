# Medi Canopy — Cannabis Information Hub

A scalable web platform for reliable cannabis market information, scientific research, courses, and consulting services. Focused on Brazil with international coverage.

**Author brand:** [@papiroebers](https://www.instagram.com/papiroebers)

## Architecture

```
medi-canopy/
├── frontend/          # Angular 16 + TypeScript SPA
├── backend/           # Python FastAPI REST API
├── agents/            # Scheduled & manual LLM agent runners
├── docs/              # Architecture, brand, agent navigation
├── scripts/           # DevOps & manual agent triggers
└── .cursor/           # Cursor skills, hooks, agents, MCP design
```

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm start
```

App: http://localhost:4200

### Run agents manually

```bash
# News agent (daily search → review queue)
python -m agents.run --agent news

# Research agent (papers → email digest)
python -m agents.run --agent research
```

### 🔧 AI AGENT (issue solver)

- Workflow: `.github/workflows/cursor-issue-solver.yml`
- Purpose: start a Cursor cloud agent for **the triggering issue only** when (1) the issue is labeled `solve`, (2) a comment starts with `[CORRECTION]`, or (3) a `[POST]` comment is left on a `daily-cannabis` issue. Comments are enough; the issue does not need `solve` for correction/post. The agent rates complexity 1–5, merges levels 1–3 into the default branch, and opens a PR only for levels 4–5. Opening or merging a pull request does not start this workflow.
- Manual test: run from Actions tab with `workflow_dispatch` (`dry_run=true` by default).
- Required repository secret: `CURSOR_API_KEY`.
- A failed Cursor launch now fails the GitHub job. Retryable `429` / GitHub App rate limits are retried automatically (Cursor often asks for ~60s).
- Cloud Agents also need the [Cursor GitHub App](https://cursor.com/dashboard?tab=integrations) installed on this repository. If retries still fail with `get_installation_for_org`, reconnect GitHub there and confirm the repo is selected.
- Research digests from `🔬 WEEKLY PAPER REPORT` run Mondays and are filed as `[RESEARCH] Daily Cannabis …` with labels `research` + `daily-cannabis`. The workflow already applies those labels when it opens the issue. Digests older than 30 days are auto-closed on each run. Previously posted papers live in `agents/data/discovered_papers.json` and are skipped on later runs; only papers from the past month are eligible. Labeling a digest `solve` does not dispatch a coding fix; comment `[POST] …` on the digest to turn a named paper into a blog post.

## Key Documents

| Document | Purpose |
|----------|---------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design & scalability plan |
| [docs/BRAND.md](docs/BRAND.md) | Color palette, typography, voice |
| [docs/AGENTS.md](docs/AGENTS.md) | Agent workflows & placeholders |
| [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) | Dev setup & conventions |
| [docs/RESOURCES_NEEDED.md](docs/RESOURCES_NEEDED.md) | APIs, keys, external services |
| [docs/AGENT_NAVIGATION.md](docs/AGENT_NAVIGATION.md) | Map for AI agents working on repo |
| [debt.txt](debt.txt) | Credentials & config placeholders |

## Design

Locked look: **Forest Canopy** palette with **V4** (minimal clean) layout. Tokens live in `frontend/src/styles/_variables.scss` and `docs/BRAND.md`.

References: [4trees Cannabis Building](https://4treesbuilding.ca/projects), [PlantManager](https://plantmanager.com.br/).

## License

Private — All rights reserved.
