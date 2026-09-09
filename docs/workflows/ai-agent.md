# AI agent

**YAML:** [`.github/workflows/cursor-issue-solver.yml`](../../.github/workflows/cursor-issue-solver.yml)
**Script:** [`scripts/run_issue_solver_agents.py`](../../scripts/run_issue_solver_agents.py)
**Secrets:** `CURSOR_API_KEY`, `GITHUB_TOKEN` (provided by Actions)

A Cursor cloud agent works an issue labeled `solve`. Complexity 1–3 is merged to the base branch; 4–5 opens a pull request. Research notes are never dispatched.

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
  classDef skip fill:#E2E8E4,stroke:#5A6B62,color:#1A1A1A
  classDef step fill:#2D6A4F,stroke:#1B4332,color:#F8FAF7

  subgraph Triggers["Triggers"]
    Labeled["issues.labeled"]:::trigger
    Manual["workflow_dispatch"]:::trigger
  end

  Gate{"Manual run, or<br/>label is solve<br/>and not a PR?"}:::decision
  SkipJob["Job skipped"]:::skip
  Job["Job: launch-issue-agents<br/>90 min timeout"]:::job
  Setup["Checkout + Python 3.11"]:::step
  Script["run_issue_solver_agents.py"]:::step

  Labeled --> Gate
  Manual --> Gate
  Gate -->|no| SkipJob
  Gate -->|yes| Job --> Setup --> Script
```

## Dispatch and outcomes

```mermaid
%%{init: {'theme':'base','themeVariables':{
  'primaryColor':'#1B4332','primaryTextColor':'#F8FAF7',
  'primaryBorderColor':'#0D1F17','lineColor':'#2D6A4F',
  'secondaryColor':'#95D5B2','tertiaryColor':'#F8FAF7',
  'fontFamily':'system-ui, sans-serif'
}}}%%
flowchart TB
  classDef step fill:#2D6A4F,stroke:#1B4332,color:#F8FAF7
  classDef decision fill:#52B788,stroke:#1B4332,color:#0D1F17
  classDef output fill:#95D5B2,stroke:#2D6A4F,color:#1A1A1A
  classDef skip fill:#E2E8E4,stroke:#5A6B62,color:#1A1A1A
  classDef ext fill:#5C4033,stroke:#0D1F17,color:#F8FAF7

  Pick["Select open solve issues<br/>or a single issue number"]:::step
  Research{"research / daily-cannabis<br/>label or title?"}:::decision
  Skip["Skip — not a coding task"]:::skip
  Cursor["Cursor cloud agent"]:::ext
  Rate{"Complexity 1-5"}:::decision
  Merge["Merge into base branch"]:::output
  PR["Open pull request<br/>do not merge"]:::output
  Comment["Comment on the issue"]:::output

  Pick --> Research
  Research -->|yes| Skip
  Research -->|no| Cursor --> Rate
  Rate -->|1 to 3| Merge
  Rate -->|4 or 5| PR
  Merge --> Comment
  PR --> Comment
```

GitHub still fires `issues.labeled` when a **pull request** is labeled, so the job `if:` also requires `github.event.issue.pull_request == null`. Manual `workflow_dispatch` defaults to `dry_run=true`.

## Manual run

Actions tab → **🔧 AI AGENT** → **Run workflow**. Leave `dry_run` true to print planned actions without calling Cursor.

More context: [AGENTS.md](../AGENTS.md).
