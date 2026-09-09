# Deploy backend

**YAML:** [`.github/workflows/deploy-backend.yml`](../../.github/workflows/deploy-backend.yml)
**Secret:** `RENDER_DEPLOY_HOOK_URL`

Netlify already builds the frontend from GitHub. Render can miss a backend rebuild after a repo rename or if Auto-Deploy is off. This workflow POSTs the Render deploy hook whenever `backend/**` lands on `main`.

```mermaid
%%{init: {'theme':'base','themeVariables':{
  'primaryColor':'#1B4332','primaryTextColor':'#F8FAF7',
  'primaryBorderColor':'#0D1F17','lineColor':'#2D6A4F',
  'secondaryColor':'#95D5B2','tertiaryColor':'#F8FAF7',
  'fontFamily':'system-ui, sans-serif'
}}}%%
flowchart TB
  classDef trigger fill:#D4A574,stroke:#5C4033,color:#1A1A1A
  classDef job fill:#1B4332,stroke:#0D1F17,color:#F8FAF7
  classDef decision fill:#52B788,stroke:#1B4332,color:#0D1F17
  classDef output fill:#95D5B2,stroke:#2D6A4F,color:#1A1A1A
  classDef skip fill:#E2E8E4,stroke:#5A6B62,color:#1A1A1A
  classDef ext fill:#5C4033,stroke:#0D1F17,color:#F8FAF7

  subgraph Triggers["Triggers"]
    Push["Push to main<br/>paths: backend/**"]:::trigger
    Manual["workflow_dispatch"]:::trigger
  end

  Job["Job: trigger-render<br/>ubuntu-latest"]:::job
  Secret{"RENDER_DEPLOY_HOOK_URL<br/>set?"}:::decision
  Skip["Warning in log<br/>exit 0 — no deploy"]:::skip
  Hook["POST deploy hook"]:::job
  Render["Render rebuilds<br/>cannahub-api"]:::ext
  Live["API live"]:::output

  Push --> Job
  Manual --> Job
  Job --> Secret
  Secret -->|missing| Skip
  Secret -->|set| Hook
  Hook --> Render
  Render --> Live
```

## What it does not do

- Does not check out the repo or run tests.
- Does not deploy the Angular frontend (Netlify).
- Missing secret is a skip, not a hard failure — the run stays green with a warning.

## Operator notes

Set the hook in GitHub → **Settings** → **Secrets and variables** → **Actions** from Render → **cannahub-api** → **Settings** → **Deploy Hook**. See [DEPLOY.md](../DEPLOY.md).
