# Agents — use backend virtualenv

Agents import from `backend/app`. Install dependencies once:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run from repository root:

```bash
backend\.venv\Scripts\python.exe -m agents.run --agent news
backend\.venv\Scripts\python.exe -m agents.run --agent research
```

Or: `.\scripts\run-agents.ps1 -Agent news`
