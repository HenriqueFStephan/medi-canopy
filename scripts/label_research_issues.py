#!/usr/bin/env python3
"""Apply the `research` label to issues marked with [RESEARCH] in the title."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


GITHUB_API_BASE = "https://api.github.com"
RESEARCH_LABEL = "research"
RESEARCH_TITLE_MARKER = "[research]"
DAILY_CANNABIS_TITLE_MARKER = "daily cannabis"
LABEL_COLOR = "0E8A16"
LABEL_DESCRIPTION = "Research note for the team — not a coding task for the issue solver"


def log(message: str, *, error: bool = False) -> None:
    stream = sys.stderr if error else sys.stdout
    print(message, file=stream, flush=True)


def _http_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str],
    payload: dict[str, Any] | list[Any] | None = None,
) -> Any:
    data = None
    request_headers = headers.copy()
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        request_headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, method=method, headers=request_headers, data=data)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {url} failed ({exc.code}): {body}") from exc


def github_headers(token: str) -> dict[str, str]:
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def is_research_title(title: str) -> bool:
    lower = (title or "").lower()
    return RESEARCH_TITLE_MARKER in lower or DAILY_CANNABIS_TITLE_MARKER in lower


def ensure_research_label(repo: str, headers: dict[str, str]) -> None:
    url = f"{GITHUB_API_BASE}/repos/{repo}/labels/{urllib.parse.quote(RESEARCH_LABEL)}"
    try:
        _http_json("GET", url, headers=headers)
        return
    except RuntimeError as exc:
        if "(404)" not in str(exc):
            raise
    _http_json(
        "POST",
        f"{GITHUB_API_BASE}/repos/{repo}/labels",
        headers=headers,
        payload={
            "name": RESEARCH_LABEL,
            "color": LABEL_COLOR,
            "description": LABEL_DESCRIPTION,
        },
    )
    log(f"Created label `{RESEARCH_LABEL}`.")


def issue_has_research_label(labels: list[Any]) -> bool:
    for label in labels:
        name = label.get("name", "") if isinstance(label, dict) else str(label)
        if name.strip().lower() in {RESEARCH_LABEL, f"[{RESEARCH_LABEL}]"}:
            return True
    return False


def apply_research_label(repo: str, issue_number: int, headers: dict[str, str]) -> bool:
    ensure_research_label(repo, headers)
    url = f"{GITHUB_API_BASE}/repos/{repo}/issues/{issue_number}/labels"
    _http_json("POST", url, headers=headers, payload={"labels": [RESEARCH_LABEL]})
    log(f"Labeled issue #{issue_number} with `{RESEARCH_LABEL}`.")
    return True


def label_single_issue(repo: str, issue_number: int, title: str, headers: dict[str, str]) -> int:
    if not is_research_title(title):
        log(f"Issue #{issue_number} title has no [RESEARCH] marker; leaving unlabeled.")
        return 0
    issue = _http_json("GET", f"{GITHUB_API_BASE}/repos/{repo}/issues/{issue_number}", headers=headers)
    if issue_has_research_label(issue.get("labels", [])):
        log(f"Issue #{issue_number} already has `{RESEARCH_LABEL}`.")
        return 0
    apply_research_label(repo, issue_number, headers)
    return 1


def backfill_open_issues(repo: str, headers: dict[str, str]) -> int:
    labeled = 0
    page = 1
    while True:
        query = urllib.parse.urlencode(
            {"state": "open", "per_page": "100", "page": str(page), "sort": "created", "direction": "asc"}
        )
        result = _http_json("GET", f"{GITHUB_API_BASE}/repos/{repo}/issues?{query}", headers=headers)
        if not isinstance(result, list) or not result:
            break
        for item in result:
            if "pull_request" in item:
                continue
            title = (item.get("title") or "").strip()
            number = int(item["number"])
            if not is_research_title(title):
                continue
            if issue_has_research_label(item.get("labels", [])):
                continue
            apply_research_label(repo, number, headers)
            labeled += 1
        if len(result) < 100:
            break
        page += 1
    return labeled


def _to_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Auto-label research issues.")
    parser.add_argument("--repo", required=True, help="owner/repo")
    parser.add_argument("--event-name", default="", help="GitHub event name")
    parser.add_argument("--issue-number", default="", help="Issue number for issues events")
    parser.add_argument("--issue-title", default="", help="Issue title for issues events")
    parser.add_argument("--backfill", default="false", help="Scan open issues for [RESEARCH] titles")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        log("Missing required env var: GITHUB_TOKEN", error=True)
        return 2

    headers = github_headers(token)
    labeled = 0

    if args.event_name == "issues" and args.issue_number.strip():
        labeled += label_single_issue(
            args.repo,
            int(args.issue_number),
            args.issue_title,
            headers,
        )

    if args.event_name == "workflow_dispatch" and _to_bool(args.backfill):
        labeled += backfill_open_issues(args.repo, headers)

    log(f"Done. Newly labeled: {labeled}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
