# AI agent

**YAML:** [`.github/workflows/cursor-issue-solver.yml`](../../.github/workflows/cursor-issue-solver.yml)
**Script:** [`scripts/run_issue_solver_agents.py`](../../scripts/run_issue_solver_agents.py)
**Secrets:** `CURSOR_API_KEY`, `GITHUB_TOKEN` (provided by Actions)

A Cursor cloud agent runs against **the issue that triggered the workflow** — it does not search for other open issues. Complexity 1–3 is merged to the base branch; 4–5 opens a pull request.

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
    Labeled["issues.labeled<br/>label is solve"]:::trigger
    Correction["issue_comment.created<br/>body starts with [CORRECTION]"]:::trigger
    Post["issue_comment.created<br/>[POST] on daily-cannabis"]:::trigger
    Manual["workflow_dispatch"]:::trigger
  end

  Gate{"Matched trigger<br/>and not a PR?"}:::decision
  SkipJob["Job skipped"]:::skip
  Job["Job: launch-issue-agents<br/>90 min timeout"]:::job
  Setup["Checkout + Python 3.11"]:::step
  Script["run_issue_solver_agents.py<br/>that issue only"]:::step

  Labeled --> Gate
  Correction --> Gate
  Post --> Gate
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

  Pick["Use the triggering issue<br/>and comment, if any"]:::step
  Kind{"Which trigger?"}:::decision
  SkipSolve["Skip research / daily-cannabis<br/>on solve"]:::skip
  Cursor["Cursor cloud agent"]:::ext
  Rate{"Complexity 1-5"}:::decision
  Merge["Merge into base branch"]:::output
  PR["Open pull request<br/>do not merge"]:::output
  Comment["Comment on the issue"]:::output

  Pick --> Kind
  Kind -->|solve on a digest| SkipSolve
  Kind -->|solve / correction / post| Cursor --> Rate
  Rate -->|1 to 3| Merge
  Rate -->|4 or 5| PR
  Merge --> Comment
  PR --> Comment
```

## What each trigger sends to the agent

| Trigger | Fires when | Prompt focus |
|---------|------------|--------------|
| `solve` | Issue labeled `solve` (including a new issue opened with that label) | Issue title, labels, and body |
| `correction` | Comment body starts with `[CORRECTION]` | The comment is the task; issue body is context only |
| `post` | Comment body starts with `[POST]` **and** the issue has `daily-cannabis` | Named paper(s); digest links are extracted and must be opened in depth before writing; every URL/DOI is copied onto the site as a clickable link |

Comments are enough to start the workflow. The issue does **not** need the `solve` label for `[CORRECTION]` or `[POST]`. Ordinary comments, and `[POST]` on issues without `daily-cannabis`, do not run the job.

GitHub still fires `issues` / `issue_comment` when the target is a **pull request**, so the job `if:` also requires `github.event.issue.pull_request == null`. Manual `workflow_dispatch` defaults to `dry_run=true` and requires an issue number.

## Manual run

Actions tab → **🔧 AI AGENT** → **Run workflow**. Set `issue_number`, optionally `trigger` and `comment_id`. Leave `dry_run` true to print planned actions without calling Cursor.

More context: [AGENTS.md](../AGENTS.md).
