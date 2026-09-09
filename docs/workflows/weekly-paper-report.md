# Weekly paper report

**YAML:** [`.github/workflows/daily-cannabis-research.yml`](../../.github/workflows/daily-cannabis-research.yml)
**Script:** [`scripts/run_daily_cannabis_research.py`](../../scripts/run_daily_cannabis_research.py)
**Catalog:** `agents/data/discovered_papers.json`
**Secrets:** `CURSOR_API_KEY`, `GITHUB_TOKEN` (provided by Actions)

Mondays at 06:30 UTC (or a manual run) a Cursor cloud agent searches peer-reviewed cannabis literature. Surviving papers become a GitHub issue; they are never auto-published.

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
  classDef step fill:#2D6A4F,stroke:#1B4332,color:#F8FAF7
  classDef decision fill:#52B788,stroke:#1B4332,color:#0D1F17
  classDef output fill:#95D5B2,stroke:#2D6A4F,color:#1A1A1A
  classDef skip fill:#E2E8E4,stroke:#5A6B62,color:#1A1A1A
  classDef ext fill:#5C4033,stroke:#0D1F17,color:#F8FAF7

  subgraph Triggers["Triggers"]
    Cron["schedule: Mondays 06:30 UTC"]:::trigger
    Manual["workflow_dispatch<br/>date, model, filters"]:::trigger
  end

  Job["Job: gather-research<br/>90 min timeout"]:::job
  Checkout["Checkout + Python 3.11"]:::step
  Params["Resolve parameters"]:::step
  Script["run_daily_cannabis_research.py"]:::step

  Cron --> Job
  Manual --> Job
  Job --> Checkout --> Params --> Script
```

## Inside the script

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

  Catalog["Load discovered_papers.json"]:::step
  Cleanup["Close research issues<br/>older than 30 days"]:::step
  OnlyCleanup{"cleanup_only?"}:::decision
  Dry{"dry_run?"}:::decision
  Cursor["Cursor cloud agent"]:::ext
  Filter["Reliability filter<br/>peer-reviewed, journal, DOI/host,<br/>last 31 days, not in catalog, confidence"]:::step
  Any{"Any papers accepted?"}:::decision
  Issue["Open GitHub issue<br/>research + daily-cannabis"]:::output
  NoIssue["No issue — empty digest is noise"]:::skip
  Commit["Commit catalog to the branch"]:::output
  Artifact["Upload agents/output/daily_cannabis/<br/>90-day artifact"]:::output
  Done["Stop"]:::skip

  Catalog --> Cleanup --> OnlyCleanup
  OnlyCleanup -->|yes| Done
  OnlyCleanup -->|no| Dry
  Dry -->|yes| Done
  Dry -->|no| Cursor --> Filter --> Any
  Any -->|yes| Issue
  Any -->|no| NoIssue
  Issue --> Commit
  NoIssue --> Artifact
  Commit --> Artifact
```

## Reliability filter

A paper reaches the issue only if it is flagged peer-reviewed, names a journal, is not a preprint/blog/thesis/patent, has a DOI or a recognised publisher host, was published in the last 31 days, is not already in the catalog, and meets `--min-confidence` (default `0.7`). Rejected candidates stay in the job summary and the artifact.

Research issues are not coding tasks. The AI agent workflow only starts on the `solve` label, so these digests are not dispatched as fixes.

## Manual run

Actions tab → **🔬 WEEKLY PAPER REPORT** → **Run workflow**, or:

```bash
python scripts/run_daily_cannabis_research.py \
  --repo owner/repo --repo-url https://github.com/owner/repo --dry-run
```

More context: [AGENTS.md](../AGENTS.md).
