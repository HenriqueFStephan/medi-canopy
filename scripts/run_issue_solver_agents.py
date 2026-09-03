#!/usr/bin/env python3
"""
Dispatch one Cursor cloud agent per open GitHub issue.

The launched agent is instructed to:
- fix exactly one issue on its own branch
- create a detailed PR
- include validation notes
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import textwrap
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


GITHUB_API_BASE = "https://api.github.com"
CURSOR_API_BASE = "https://api.cursor.com/v1"


@dataclass
class Issue:
    number: int
    title: str
    body: str
    html_url: str
    labels: list[str]


def _http_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any] | list[Any]:
    data = None
    request_headers = headers.copy() if headers else {}
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
    except urllib.error.URLError as exc:
        raise RuntimeError(f"{method} {url} failed: {exc.reason}") from exc


def fetch_open_issues(repo: str, github_token: str, limit: int) -> list[Issue]:
    query = urllib.parse.urlencode({"state": "open", "per_page": str(min(max(limit, 1), 100))})
    url = f"{GITHUB_API_BASE}/repos/{repo}/issues?{query}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    result = _http_json("GET", url, headers=headers)
    if not isinstance(result, list):
        raise RuntimeError(f"Unexpected GitHub response for issues: {type(result)}")

    issues: list[Issue] = []
    for item in result:
        # GitHub issues endpoint also returns PRs; skip those.
        if "pull_request" in item:
            continue
        issues.append(
            Issue(
                number=int(item["number"]),
                title=item.get("title", "").strip(),
                body=(item.get("body") or "").strip(),
                html_url=item.get("html_url", ""),
                labels=[label.get("name", "") for label in item.get("labels", []) if isinstance(label, dict)],
            )
        )
        if len(issues) >= limit:
            break
    return issues


def build_prompt(issue: Issue, repo: str, base_ref: str) -> str:
    labels = ", ".join(issue.labels) if issue.labels else "none"
    issue_body = issue.body if issue.body else "(no description provided)"
    return textwrap.dedent(
        f"""
        You are working on repository {repo}.
        Solve GitHub issue #{issue.number} on a dedicated branch and open a pull request.

        Constraints:
        - Touch only code relevant to issue #{issue.number}.
        - Keep scope focused and minimal.
        - Add or update tests when feasible.
        - Base branch: {base_ref}.
        - The PR must be review-ready and include detailed context.

        Issue metadata:
        - URL: {issue.html_url}
        - Title: {issue.title}
        - Labels: {labels}
        - Description:
        {issue_body}

        PR requirements:
        - Title format: "fix(issue #{issue.number}): <short summary>"
        - Body sections, in order:
          1) Summary
          2) Root Cause
          3) Changes Made
          4) Validation (tests/manual checks)
          5) Risks / Follow-ups
          6) Closes #{issue.number}
        - Mention changed files and why each was changed.

        Before finishing:
        - Run relevant checks/tests for changed components.
        - Ensure formatting/lint expectations still pass for touched files.
        """
    ).strip()


def create_cursor_agent(
    *,
    cursor_api_key: str,
    model: str,
    repo_url: str,
    base_ref: str,
    prompt: str,
    run_name: str,
    skip_reviewer_request: bool,
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
        "autoCreatePR": True,
        "skipReviewerRequest": skip_reviewer_request,
    }
    return _http_json("POST", f"{CURSOR_API_BASE}/agents", headers=headers, payload=payload)


def _to_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Launch Cursor cloud agents to solve open GitHub issues.")
    parser.add_argument("--repo", required=True, help="owner/repo")
    parser.add_argument("--repo-url", required=True, help="Git clone URL, e.g. https://github.com/org/repo")
    parser.add_argument("--base-ref", required=True, help="Base branch used by cloud agents")
    parser.add_argument("--max-issues", type=int, default=1, help="Maximum number of issues to process")
    parser.add_argument("--model", default="composer-2.5", help="Cursor model id")
    parser.add_argument("--dry-run", action="store_true", help="Only print planned operations")
    parser.add_argument(
        "--skip-reviewer-request",
        action="store_true",
        help="Set Cursor skipReviewerRequest=true when opening PRs",
    )
    args = parser.parse_args()

    github_token = os.environ.get("GITHUB_TOKEN")
    cursor_api_key = os.environ.get("CURSOR_API_KEY")
    if not github_token:
        print("Missing required env var: GITHUB_TOKEN", file=sys.stderr)
        return 2
    if not cursor_api_key and not args.dry_run:
        print("Missing required env var: CURSOR_API_KEY", file=sys.stderr)
        return 2

    if args.max_issues < 1:
        print("--max-issues must be >= 1", file=sys.stderr)
        return 2

    try:
        issues = fetch_open_issues(args.repo, github_token, args.max_issues)
    except RuntimeError as exc:
        print(f"Failed fetching issues: {exc}", file=sys.stderr)
        return 1

    if not issues:
        print("No open issues found.")
        return 0

    print(f"Found {len(issues)} open issue(s) to process.")
    for issue in issues:
        prompt = build_prompt(issue, args.repo, args.base_ref)
        run_name = f"Issue #{issue.number}: {issue.title[:80]}"

        if args.dry_run:
            print(f"[DRY RUN] Would launch agent for issue #{issue.number}: {issue.title}")
            continue

        try:
            response = create_cursor_agent(
                cursor_api_key=cursor_api_key or "",
                model=args.model,
                repo_url=args.repo_url,
                base_ref=args.base_ref,
                prompt=prompt,
                run_name=run_name,
                skip_reviewer_request=args.skip_reviewer_request,
            )
        except RuntimeError as exc:
            print(f"Issue #{issue.number} launch failed: {exc}", file=sys.stderr)
            continue

        agent_id = response.get("id")
        agent_url = response.get("url")
        print(f"Issue #{issue.number} -> agent {agent_id or '(unknown id)'}")
        if agent_url:
            print(f"  URL: {agent_url}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
