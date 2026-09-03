#!/usr/bin/env python3
"""
Launch a Cursor cloud agent that gathers the latest peer-reviewed cannabis research.

Coverage spans medical use, hemp fibre in fashion/textiles, construction materials,
agronomy, and policy. Only peer-reviewed, verifiable papers survive the reliability
filter; the surviving links are published as a GitHub issue titled
"Daily Cannabis {date}".
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import textwrap
import time
import urllib.parse
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from run_issue_solver_agents import (  # noqa: E402
    CURSOR_API_BASE,
    GITHUB_API_BASE,
    ApiError,
    _http_json,
    log,
)

DEFAULT_MODEL = "composer-2.5"
# Keep in sync with DEFAULT_EXCLUDED_LABELS in run_issue_solver_agents.py so the
# issue solver never tries to "fix" one of these digests.
DEFAULT_ISSUE_LABELS = ("daily-cannabis", "research")
DEFAULT_MIN_CONFIDENCE = 0.7
DEFAULT_MAX_PAPERS = 12
DEFAULT_POLL_INTERVAL_SECONDS = 30
DEFAULT_TIMEOUT_SECONDS = 3600

TERMINAL_STATUSES = {"FINISHED", "ERROR", "CANCELLED", "EXPIRED"}

RESEARCH_TOPICS = [
    "Medical and clinical use (cannabinoids, CBD/THC trials, therapeutic outcomes, safety)",
    "Hemp fibre in fashion and textiles (yarn, fabric, dyeing, life-cycle assessment)",
    "Hemp in construction (hempcrete, bio-composites, insulation, structural performance)",
    "Agronomy and cultivation science (breeding, yield, controlled environments)",
    "Regulation and public-health policy evaluation",
]

# Sources that publish without peer review; papers from these are rejected.
PREPRINT_HOSTS = {
    "arxiv.org",
    "biorxiv.org",
    "medrxiv.org",
    "chemrxiv.org",
    "preprints.org",
    "ssrn.com",
    "papers.ssrn.com",
    "researchsquare.com",
    "osf.io",
    "zenodo.org",
}

# Hosts accepted as evidence of a real scholarly record when no DOI is supplied.
SCHOLARLY_HOSTS = {
    "doi.org",
    "dx.doi.org",
    "pubmed.ncbi.nlm.nih.gov",
    "ncbi.nlm.nih.gov",
    "pmc.ncbi.nlm.nih.gov",
    "sciencedirect.com",
    "springer.com",
    "link.springer.com",
    "nature.com",
    "wiley.com",
    "onlinelibrary.wiley.com",
    "tandfonline.com",
    "sagepub.com",
    "journals.sagepub.com",
    "mdpi.com",
    "frontiersin.org",
    "bmj.com",
    "thelancet.com",
    "jamanetwork.com",
    "nejm.org",
    "cambridge.org",
    "oup.com",
    "academic.oup.com",
    "acs.org",
    "pubs.acs.org",
    "rsc.org",
    "pubs.rsc.org",
    "plos.org",
    "journals.plos.org",
    "karger.com",
    "liebertpub.com",
    "scielo.br",
    "scielo.org",
    "elsevier.com",
    "iopscience.iop.org",
    "asme.org",
    "ascelibrary.org",
}

NON_PEER_REVIEWED_TYPES = {
    "preprint",
    "blog",
    "news",
    "press-release",
    "magazine",
    "thesis",
    "dissertation",
    "white-paper",
    "report",
    "conference-abstract",
    "patent",
}

DOI_PATTERN = re.compile(r"^10\.\d{4,9}/\S+$")
JSON_BLOCK_PATTERN = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)


@dataclass
class Paper:
    title: str
    url: str
    journal: str = ""
    authors: str = ""
    year: int | None = None
    doi: str = ""
    category: str = "uncategorized"
    publication_type: str = ""
    peer_reviewed: bool = False
    confidence: float = 0.0
    summary: str = ""

    def dedupe_key(self) -> str:
        if self.doi:
            return f"doi:{self.doi.lower()}"
        return f"url:{normalize_url(self.url)}"


@dataclass
class FilterOutcome:
    accepted: list[Paper] = field(default_factory=list)
    rejected: list[tuple[Paper, str]] = field(default_factory=list)


def utc_date(explicit: str | None = None) -> str:
    if explicit:
        return explicit
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def normalize_url(url: str) -> str:
    cleaned = (url or "").strip().rstrip("/")
    cleaned = re.sub(r"^https?://", "", cleaned, flags=re.IGNORECASE)
    return re.sub(r"^www\.", "", cleaned, flags=re.IGNORECASE).lower()


def url_host(url: str) -> str:
    return normalize_url(url).split("/", 1)[0]


def host_matches(host: str, candidates: set[str]) -> bool:
    return any(host == candidate or host.endswith(f".{candidate}") for candidate in candidates)


def build_prompt(date_str: str, max_papers: int, min_confidence: float) -> str:
    topics = "\n".join(f"        - {topic}" for topic in RESEARCH_TOPICS)
    return textwrap.dedent(
        f"""
        You are a research librarian building the "Daily Cannabis {date_str}" digest.

        Goal: find the most recent peer-reviewed scientific literature about cannabis
        and industrial hemp across these areas:
{topics}

        Hard requirements — a paper is only eligible if ALL of these hold:
        - It is published in a peer-reviewed journal. Preprints (arXiv, bioRxiv, medRxiv,
          SSRN, Research Square, preprints.org), theses, patents, blogs, press releases,
          conference abstracts and news articles are NOT eligible.
        - It has a resolvable DOI, or a canonical link on a recognised publisher/index
          domain (doi.org, PubMed, PMC, ScienceDirect, Springer, Nature, Wiley, MDPI,
          Frontiers, SAGE, Taylor & Francis, PLOS, SciELO, Oxford, Cambridge, ACS, RSC...).
        - You verified the record actually exists; never invent a DOI, title or link.
        - It is recent: prefer the last 12 months, and never older than 3 years.

        Reliability: assign each paper a `confidence` between 0 and 1 reflecting how sure
        you are that the record is real, peer-reviewed and correctly described. Report a low
        confidence instead of guessing. Papers below {min_confidence} will be discarded, and
        it is far better to return fewer papers than to return an unreliable one. Returning
        an empty list is an acceptable outcome.

        Return at most {max_papers} papers.

        Output format — reply with a single fenced ```json block and nothing else:

        ```json
        {{
          "generated_for": "{date_str}",
          "papers": [
            {{
              "title": "Full paper title",
              "authors": "First Author et al.",
              "journal": "Journal name",
              "year": 2026,
              "doi": "10.1000/example",
              "url": "https://doi.org/10.1000/example",
              "category": "medical | textile | construction | agronomy | policy",
              "publication_type": "journal-article",
              "peer_reviewed": true,
              "confidence": 0.93,
              "summary": "One or two sentences on the finding and why it matters."
            }}
          ]
        }}
        ```

        Do not modify any files in the repository and do not open a pull request.
        Your entire deliverable is the JSON block above.
        """
    ).strip()


def create_research_agent(
    *,
    cursor_api_key: str,
    model: str,
    repo_url: str,
    base_ref: str,
    prompt: str,
    run_name: str,
) -> dict[str, Any]:
    token = base64.b64encode(f"{cursor_api_key}:".encode("utf-8")).decode("ascii")
    headers = {
        "Authorization": f"Basic {token}",
        "Accept": "application/json",
    }
    payload: dict[str, Any] = {
        "name": run_name,
        "prompt": {"text": prompt},
        "model": {"id": model},
        "repos": [{"url": repo_url, "startingRef": base_ref}],
        "autoCreatePR": False,
    }
    return _http_json("POST", f"{CURSOR_API_BASE}/agents", headers=headers, payload=payload)


def get_run(*, cursor_api_key: str, agent_id: str, run_id: str) -> dict[str, Any]:
    token = base64.b64encode(f"{cursor_api_key}:".encode("utf-8")).decode("ascii")
    headers = {
        "Authorization": f"Basic {token}",
        "Accept": "application/json",
    }
    result = _http_json("GET", f"{CURSOR_API_BASE}/agents/{agent_id}/runs/{run_id}", headers=headers)
    if not isinstance(result, dict):
        raise ApiError(f"Unexpected Cursor run response: {type(result)}")
    return result


def wait_for_run(
    *,
    cursor_api_key: str,
    agent_id: str,
    run_id: str,
    poll_interval: int,
    timeout: int,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    last_status = ""
    while True:
        run = get_run(cursor_api_key=cursor_api_key, agent_id=agent_id, run_id=run_id)
        status = str(run.get("status") or "").upper()
        if status != last_status:
            log(f"Run {run_id} status: {status or 'UNKNOWN'}")
            last_status = status
        if status in TERMINAL_STATUSES:
            return run
        if time.monotonic() >= deadline:
            raise ApiError(f"Timed out after {timeout}s waiting for run {run_id} (last status: {status})")
        time.sleep(max(poll_interval, 1))


def extract_json_payload(text: str) -> dict[str, Any]:
    """Pull the JSON object out of an assistant reply that may wrap it in prose/fences."""
    if not text or not text.strip():
        raise ValueError("Agent returned an empty result")

    candidates: list[str] = [match.group(1) for match in JSON_BLOCK_PATTERN.finditer(text)]

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end > start:
        candidates.append(text[start : end + 1])

    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed

    raise ValueError("Could not find a JSON object in the agent result")


def _coerce_year(value: Any) -> int | None:
    try:
        year = int(str(value).strip()[:4])
    except (TypeError, ValueError):
        return None
    return year if 1900 <= year <= 2200 else None


def _coerce_confidence(value: Any) -> float:
    try:
        confidence = float(value)
    except (TypeError, ValueError):
        return 0.0
    # Tolerate agents reporting confidence as a percentage.
    if confidence > 1.0:
        confidence = confidence / 100.0
    return max(0.0, min(1.0, confidence))


def parse_papers(payload: dict[str, Any]) -> list[Paper]:
    raw_papers = payload.get("papers")
    if not isinstance(raw_papers, list):
        raise ValueError("Agent JSON payload has no 'papers' list")

    papers: list[Paper] = []
    for raw in raw_papers:
        if not isinstance(raw, dict):
            continue
        doi = str(raw.get("doi") or "").strip()
        doi = re.sub(r"^(?:https?://)?(?:dx\.)?doi\.org/", "", doi, flags=re.IGNORECASE)
        papers.append(
            Paper(
                title=str(raw.get("title") or "").strip(),
                url=str(raw.get("url") or "").strip(),
                journal=str(raw.get("journal") or "").strip(),
                authors=str(raw.get("authors") or "").strip(),
                year=_coerce_year(raw.get("year")),
                doi=doi,
                category=str(raw.get("category") or "uncategorized").strip().lower(),
                publication_type=str(raw.get("publication_type") or "").strip().lower(),
                peer_reviewed=bool(raw.get("peer_reviewed")),
                confidence=_coerce_confidence(raw.get("confidence")),
                summary=str(raw.get("summary") or "").strip(),
            )
        )
    return papers


def rejection_reason(paper: Paper, min_confidence: float) -> str | None:
    """Return why a paper is not publishable, or None when it passes every check."""
    if not paper.title:
        return "missing title"
    if not paper.url:
        return "missing link"
    if not re.match(r"^https?://", paper.url, flags=re.IGNORECASE):
        return "link is not a valid http(s) URL"
    if not paper.peer_reviewed:
        return "not flagged as peer-reviewed"
    if paper.publication_type in NON_PEER_REVIEWED_TYPES:
        return f"publication type '{paper.publication_type}' is not peer-reviewed"
    if not paper.journal:
        return "missing journal name"

    host = url_host(paper.url)
    if host_matches(host, PREPRINT_HOSTS):
        return f"hosted on preprint/repository domain '{host}'"

    has_valid_doi = bool(paper.doi) and bool(DOI_PATTERN.match(paper.doi))
    if not has_valid_doi and not host_matches(host, SCHOLARLY_HOSTS):
        return f"no valid DOI and '{host}' is not a recognised scholarly domain"

    if paper.confidence < min_confidence:
        return f"confidence {paper.confidence:.2f} below threshold {min_confidence:.2f}"
    return None


def filter_reliable_papers(papers: list[Paper], min_confidence: float) -> FilterOutcome:
    outcome = FilterOutcome()
    seen: set[str] = set()
    for paper in papers:
        reason = rejection_reason(paper, min_confidence)
        if reason:
            outcome.rejected.append((paper, reason))
            continue
        key = paper.dedupe_key()
        if key in seen:
            outcome.rejected.append((paper, "duplicate of an earlier entry"))
            continue
        seen.add(key)
        outcome.accepted.append(paper)
    outcome.accepted.sort(key=lambda p: (-p.confidence, p.title.lower()))
    return outcome


def _render_accepted_sections(outcome: FilterOutcome) -> list[str]:
    lines: list[str] = []
    by_category: dict[str, list[Paper]] = {}
    for paper in outcome.accepted:
        by_category.setdefault(paper.category or "uncategorized", []).append(paper)

    for category in sorted(by_category):
        lines.append(f"## {category.title()}")
        lines.append("")
        for paper in by_category[category]:
            meta = " · ".join(
                part
                for part in (paper.journal, str(paper.year) if paper.year else "", paper.authors)
                if part
            )
            lines.append(f"- [{paper.title}]({paper.url})")
            if meta:
                lines.append(f"  - {meta}")
            if paper.doi:
                lines.append(f"  - DOI: `{paper.doi}`")
            lines.append(f"  - Confidence: {paper.confidence:.2f}")
            if paper.summary:
                lines.append(f"  - {paper.summary}")
        lines.append("")
    return lines


def render_issue_body(date_str: str, outcome: FilterOutcome, *, agent_url: str = "") -> str:
    """Issue body carrying only papers that cleared every reliability check.

    Discarded candidates are deliberately reduced to a count: the issue must not
    surface links that failed verification.
    """
    count = len(outcome.accepted)
    lines = [
        f"{count} peer-reviewed paper{'s' if count != 1 else ''} cleared the reliability checks "
        f"for {date_str}.",
        "",
    ]
    lines.extend(_render_accepted_sections(outcome))

    if outcome.rejected:
        discarded = len(outcome.rejected)
        noun = "candidate was" if discarded == 1 else "candidates were"
        lines.append(
            f"_{discarded} further {noun} discarded for failing the "
            "peer-review or verifiability checks._"
        )
        lines.append("")

    if agent_url:
        lines.append(f"[View Cursor agent run]({agent_url})")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_summary(date_str: str, outcome: FilterOutcome, *, agent_url: str = "") -> str:
    """Full diagnostic report for the job summary and archived artifact."""
    lines = [f"# Daily Cannabis {date_str}", ""]

    if not outcome.accepted:
        lines.append("No peer-reviewed papers cleared the reliability checks today.")
        lines.append("")
    else:
        count = len(outcome.accepted)
        lines.append(f"{count} peer-reviewed paper{'s' if count != 1 else ''} passed the reliability checks.")
        lines.append("")
        lines.extend(_render_accepted_sections(outcome))

    if outcome.rejected:
        lines.append("<details><summary>Discarded as unreliable "
                     f"({len(outcome.rejected)})</summary>")
        lines.append("")
        for paper, reason in outcome.rejected:
            label = paper.title or paper.url or "(untitled entry)"
            lines.append(f"- {label} — {reason}")
        lines.append("")
        lines.append("</details>")
        lines.append("")

    if agent_url:
        lines.append(f"[View Cursor agent run]({agent_url})")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def issue_title(date_str: str) -> str:
    return f"Daily Cannabis {date_str}"


def _github_headers(github_token: str) -> dict[str, str]:
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def find_issue_by_title(repo: str, github_token: str, title: str, *, max_pages: int = 2) -> dict[str, Any] | None:
    """Return an existing issue with this exact title, so re-runs do not duplicate it."""
    for page in range(1, max_pages + 1):
        query = urllib.parse.urlencode(
            {"state": "all", "per_page": "100", "page": str(page), "sort": "created", "direction": "desc"}
        )
        result = _http_json(
            "GET",
            f"{GITHUB_API_BASE}/repos/{repo}/issues?{query}",
            headers=_github_headers(github_token),
        )
        if not isinstance(result, list):
            raise ApiError(f"Unexpected GitHub response for issues: {type(result)}")
        if not result:
            return None
        for item in result:
            if not isinstance(item, dict) or "pull_request" in item:
                continue
            if (item.get("title") or "").strip() == title:
                return item
        if len(result) < 100:
            return None
    return None


def create_github_issue(
    repo: str,
    github_token: str,
    *,
    title: str,
    body: str,
    labels: list[str],
) -> dict[str, Any]:
    payload: dict[str, Any] = {"title": title, "body": body}
    if labels:
        payload["labels"] = labels
    result = _http_json(
        "POST",
        f"{GITHUB_API_BASE}/repos/{repo}/issues",
        headers=_github_headers(github_token),
        payload=payload,
    )
    if not isinstance(result, dict):
        raise ApiError(f"Unexpected GitHub response creating issue: {type(result)}")
    return result


def publish_issue(
    *,
    repo: str,
    github_token: str,
    date_str: str,
    outcome: FilterOutcome,
    labels: list[str],
    agent_url: str = "",
) -> str:
    """Create the 'Daily Cannabis {date}' issue and return its URL."""
    title = issue_title(date_str)
    existing = find_issue_by_title(repo, github_token, title)
    if existing:
        url = str(existing.get("html_url") or "")
        log(f"Issue '{title}' already exists; leaving it untouched ({url})")
        return url

    issue = create_github_issue(
        repo,
        github_token,
        title=title,
        body=render_issue_body(date_str, outcome, agent_url=agent_url),
        labels=labels,
    )
    url = str(issue.get("html_url") or "")
    log(f"Created issue '{title}' -> {url}")
    return url


def write_outputs(
    *,
    date_str: str,
    summary_markdown: str,
    outcome: FilterOutcome,
    output_dir: Path | None,
) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as fh:
            fh.write(summary_markdown)
        log(f"Wrote job summary to {summary_path}")

    if output_dir is None:
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{date_str}_daily_cannabis.md").write_text(summary_markdown, encoding="utf-8")
    payload = {
        "title": f"Daily Cannabis {date_str}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "accepted": [paper.__dict__ for paper in outcome.accepted],
        "rejected": [{"paper": paper.__dict__, "reason": reason} for paper, reason in outcome.rejected],
    }
    (output_dir / f"{date_str}_daily_cannabis.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    log(f"Wrote report files to {output_dir}")


def run_agent_and_collect(args: argparse.Namespace, cursor_api_key: str, date_str: str) -> tuple[list[Paper], str]:
    prompt = build_prompt(date_str, args.max_papers, args.min_confidence)
    run_name = f"Daily Cannabis {date_str}"

    response = create_research_agent(
        cursor_api_key=cursor_api_key,
        model=args.model,
        repo_url=args.repo_url,
        base_ref=args.base_ref,
        prompt=prompt,
        run_name=run_name,
    )
    if not isinstance(response, dict):
        raise ApiError(f"Unexpected Cursor response: {type(response)}")

    agent = response.get("agent") if isinstance(response.get("agent"), dict) else {}
    run = response.get("run") if isinstance(response.get("run"), dict) else {}
    agent_id = str(agent.get("id") or response.get("id") or "")
    run_id = str(run.get("id") or agent.get("latestRunId") or "")
    if not agent_id or not run_id:
        raise ApiError(f"Cursor did not return agent/run ids: {json.dumps(response)[:2000]}")

    agent_url = str(agent.get("url") or response.get("url") or f"https://cursor.com/agents/{agent_id}")
    log(f"Launched agent {agent_id} (run {run_id}) -> {agent_url}")

    final_run = wait_for_run(
        cursor_api_key=cursor_api_key,
        agent_id=agent_id,
        run_id=run_id,
        poll_interval=args.poll_interval,
        timeout=args.timeout,
    )
    status = str(final_run.get("status") or "").upper()
    if status != "FINISHED":
        raise ApiError(f"Run {run_id} ended with status {status}")

    payload = extract_json_payload(str(final_run.get("result") or ""))
    return parse_papers(payload), agent_url


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect peer-reviewed cannabis research via a Cursor cloud agent."
    )
    parser.add_argument("--repo-url", required=True, help="Git repo URL the agent starts from")
    parser.add_argument("--repo", default=None, help="owner/repo that receives the 'Daily Cannabis' issue")
    parser.add_argument("--base-ref", default="main", help="Base branch for the agent workspace")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Cursor model id")
    parser.add_argument("--date", default=None, help="Override the report date (YYYY-MM-DD)")
    parser.add_argument("--max-papers", type=int, default=DEFAULT_MAX_PAPERS)
    parser.add_argument(
        "--min-confidence",
        type=float,
        default=DEFAULT_MIN_CONFIDENCE,
        help="Reject papers whose reported confidence is below this value",
    )
    parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL_SECONDS)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--output-dir", default=None, help="Directory for the markdown/JSON report")
    parser.add_argument(
        "--result-file",
        default=None,
        help="Read the agent JSON result from a file instead of calling Cursor (testing)",
    )
    parser.add_argument(
        "--issue-label",
        action="append",
        default=None,
        help=f"Label applied to the issue (repeatable). Defaults to: {', '.join(DEFAULT_ISSUE_LABELS)}",
    )
    parser.add_argument(
        "--no-issue",
        action="store_true",
        help="Skip GitHub issue creation and only write the report files",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the prompt and exit")
    args = parser.parse_args()

    issue_labels = list(args.issue_label if args.issue_label is not None else DEFAULT_ISSUE_LABELS)

    date_str = utc_date(args.date)
    output_dir = Path(args.output_dir) if args.output_dir else None

    if args.dry_run:
        log(f"[DRY RUN] Would launch agent 'Daily Cannabis {date_str}' with prompt:\n")
        log(build_prompt(date_str, args.max_papers, args.min_confidence))
        return 0

    agent_url = ""
    if args.result_file:
        payload = extract_json_payload(Path(args.result_file).read_text(encoding="utf-8"))
        papers = parse_papers(payload)
    else:
        cursor_api_key = os.environ.get("CURSOR_API_KEY")
        if not cursor_api_key:
            log("Missing required env var: CURSOR_API_KEY", error=True)
            return 2
        try:
            papers, agent_url = run_agent_and_collect(args, cursor_api_key, date_str)
        except (ApiError, ValueError) as exc:
            log(f"Daily Cannabis {date_str} failed: {exc}", error=True)
            return 1

    outcome = filter_reliable_papers(papers, args.min_confidence)
    summary_markdown = render_summary(date_str, outcome, agent_url=agent_url)
    write_outputs(
        date_str=date_str,
        summary_markdown=summary_markdown,
        outcome=outcome,
        output_dir=output_dir,
    )

    log(
        f"Daily Cannabis {date_str}: {len(outcome.accepted)} accepted, "
        f"{len(outcome.rejected)} discarded."
    )

    if args.no_issue or not args.repo:
        return 0

    if not outcome.accepted:
        # Requirement: publish links only when they are reliable. An empty digest
        # would be noise, so no issue is opened today.
        log("No reliable papers today; skipping issue creation.")
        return 0

    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        log("Missing required env var: GITHUB_TOKEN (needed to open the issue)", error=True)
        return 2

    try:
        publish_issue(
            repo=args.repo,
            github_token=github_token,
            date_str=date_str,
            outcome=outcome,
            labels=issue_labels,
            agent_url=agent_url,
        )
    except ApiError as exc:
        log(f"Failed to publish 'Daily Cannabis {date_str}' issue: {exc}", error=True)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
