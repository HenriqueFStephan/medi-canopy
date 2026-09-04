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
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


GITHUB_API_BASE = "https://api.github.com"
CURSOR_API_BASE = "https://api.cursor.com/v1"
MAX_LAUNCH_ATTEMPTS = 5
MAX_RETRY_WAIT_SECONDS = 180
DEFAULT_RETRY_WAIT_SECONDS = 60
LAUNCH_SPACING_SECONDS = 60
SKIP_LABELS = frozenset({"research", "[research]"})
RESEARCH_TITLE_MARKER = "[research]"
RESEARCH_LABEL = "research"


@dataclass
class Issue:
    number: int
    title: str
    body: str
    html_url: str
    labels: list[str]


class ApiError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        retryable: bool = False,
        retry_after: int | None = None,
        body: str = "",
    ) -> None:
        super().__init__(message)
        self.status = status
        self.retryable = retryable
        self.retry_after = retry_after
        self.body = body


def log(message: str, *, error: bool = False) -> None:
    stream = sys.stderr if error else sys.stdout
    print(message, file=stream, flush=True)


def _walk_values(value: Any) -> Any:
    if isinstance(value, dict):
        yield value
        for nested in value.values():
            yield from _walk_values(nested)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_values(item)


def _parse_retry_after(raw: str | None) -> int | None:
    if not raw:
        return None
    try:
        seconds = int(float(raw.strip()))
    except ValueError:
        return None
    return max(1, seconds)


def _error_hints(payload: Any) -> tuple[bool, int | None]:
    retryable = False
    retry_after: int | None = None
    for node in _walk_values(payload):
        if node.get("isRetryable") is True or node.get("is_retryable") is True:
            retryable = True
        extra = node.get("additionalInfo") or node.get("additional_info") or {}
        if isinstance(extra, dict):
            parsed = _parse_retry_after(str(extra.get("retryAfter") or extra.get("retry_after") or ""))
            if parsed is not None:
                retry_after = parsed
        parsed = _parse_retry_after(str(node.get("retryAfter") or node.get("retry_after") or ""))
        if parsed is not None:
            retry_after = parsed
        if str(node.get("error") or "") == "ERROR_RATE_LIMITED":
            retryable = True
        if str(node.get("code") or "") in {"resource_exhausted", "rate_limited"}:
            retryable = True
    return retryable, retry_after


def _http_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
    debug: bool = False,
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
            if debug:
                log(f"{method} {url} -> HTTP {resp.status}")
                log(f"Cursor response body:\n{raw[:8000] if raw else '(empty)'}")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        parsed: Any = None
        try:
            parsed = json.loads(body) if body else None
        except json.JSONDecodeError:
            parsed = None
        retryable, retry_after = _error_hints(parsed)
        header_retry = _parse_retry_after(exc.headers.get("Retry-After") if exc.headers else None)
        if header_retry is not None:
            retry_after = header_retry
        if exc.code in {429, 503}:
            retryable = True
            retry_after = retry_after or DEFAULT_RETRY_WAIT_SECONDS
        raise ApiError(
            f"{method} {url} failed ({exc.code}): {body}",
            status=exc.code,
            retryable=retryable,
            retry_after=retry_after,
            body=body,
        ) from exc
    except urllib.error.URLError as exc:
        raise ApiError(f"{method} {url} failed: {exc.reason}", retryable=True) from exc


def skip_reason(issue: Issue) -> str | None:
    """Research notes are tracked as issues for the team, not as coding work."""
    labels = {label.strip().lower() for label in issue.labels}
    matched = labels & SKIP_LABELS
    if matched:
        return f"label {sorted(matched)[0]}"
    if RESEARCH_TITLE_MARKER in issue.title.lower():
        return "title marker [RESEARCH]"
    return None


def ensure_research_label(repo: str, headers: dict[str, str]) -> None:
    url = f"{GITHUB_API_BASE}/repos/{repo}/labels/{urllib.parse.quote(RESEARCH_LABEL)}"
    try:
        _http_json("GET", url, headers=headers)
        return
    except ApiError as exc:
        if exc.status != 404:
            raise
    _http_json(
        "POST",
        f"{GITHUB_API_BASE}/repos/{repo}/labels",
        headers=headers,
        payload={
            "name": RESEARCH_LABEL,
            "color": "0E8A16",
            "description": "Research note for the team — not a coding task for the issue solver",
        },
    )
    log(f"Created label `{RESEARCH_LABEL}`.")


def stamp_research_label(repo: str, issue: Issue, headers: dict[str, str]) -> None:
    """Promote a [RESEARCH] title marker into the durable `research` label."""
    if RESEARCH_LABEL in {label.strip().lower() for label in issue.labels}:
        return
    if RESEARCH_TITLE_MARKER not in issue.title.lower():
        return
    try:
        ensure_research_label(repo, headers)
        _http_json(
            "POST",
            f"{GITHUB_API_BASE}/repos/{repo}/issues/{issue.number}/labels",
            headers=headers,
            payload={"labels": [RESEARCH_LABEL]},
        )
        log(f"Stamped `{RESEARCH_LABEL}` on issue #{issue.number}.")
    except ApiError as exc:
        log(f"Could not stamp `{RESEARCH_LABEL}` on issue #{issue.number}: {exc}", error=True)


def fetch_open_issues(repo: str, github_token: str, limit: int) -> list[Issue]:
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    issues: list[Issue] = []
    skipped = 0
    page = 1
    while len(issues) < limit:
        query = urllib.parse.urlencode(
            {
                "state": "open",
                "per_page": "100",
                "page": str(page),
                "sort": "created",
                "direction": "asc",
            }
        )
        url = f"{GITHUB_API_BASE}/repos/{repo}/issues?{query}"
        result = _http_json("GET", url, headers=headers)
        if not isinstance(result, list):
            raise ApiError(f"Unexpected GitHub response for issues: {type(result)}")
        if not result:
            break

        page_items = 0
        for item in result:
            page_items += 1
            # GitHub issues endpoint also returns PRs; skip those.
            if "pull_request" in item:
                continue
            issue = Issue(
                number=int(item["number"]),
                title=item.get("title", "").strip(),
                body=(item.get("body") or "").strip(),
                html_url=item.get("html_url", ""),
                labels=[label.get("name", "") for label in item.get("labels", []) if isinstance(label, dict)],
            )
            reason = skip_reason(issue)
            if reason:
                skipped += 1
                log(f"Skipping issue #{issue.number} ({reason}): {issue.title}")
                if "title marker" in reason:
                    stamp_research_label(repo, issue, headers)
                continue
            issues.append(issue)
            if len(issues) >= limit:
                break

        if page_items < 100:
            break
        page += 1

    if skipped:
        log(f"Skipped {skipped} research/note issue(s).")
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
    return _http_json(
        "POST",
        f"{CURSOR_API_BASE}/agents",
        headers=headers,
        payload=payload,
        debug=True,
    )


def _first_text(*values: Any) -> str | None:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
        if value is not None and not isinstance(value, (dict, list)):
            text = str(value).strip()
            if text:
                return text
    return None


def agent_identity(response: dict[str, Any]) -> tuple[str | None, str | None]:
    agent = response.get("agent") if isinstance(response.get("agent"), dict) else {}
    run = response.get("run") if isinstance(response.get("run"), dict) else {}
    target = agent.get("target") if isinstance(agent.get("target"), dict) else response.get("target")
    if not isinstance(target, dict):
        target = {}

    agent_id = _first_text(
        agent.get("id"),
        response.get("id"),
        response.get("agentId"),
        response.get("agent_id"),
        run.get("agentId"),
        run.get("agent_id"),
    )
    agent_url = _first_text(
        agent.get("url"),
        target.get("url"),
        response.get("url"),
        target.get("prUrl"),
        run.get("url"),
    )
    if agent_id and not agent_url:
        agent_url = f"https://cursor.com/agents/{agent_id}"
    return agent_id, agent_url


def _sleep(seconds: int, reason: str) -> None:
    wait = min(max(seconds, 1), MAX_RETRY_WAIT_SECONDS)
    log(f"Waiting {wait}s ({reason})")
    time.sleep(wait)


def create_cursor_agent_with_retry(**kwargs: Any) -> dict[str, Any]:
    last_error: ApiError | None = None
    for attempt in range(1, MAX_LAUNCH_ATTEMPTS + 1):
        try:
            response = create_cursor_agent(**kwargs)
            if not isinstance(response, dict):
                raise ApiError(f"Unexpected Cursor response: {type(response)}")
            return response
        except ApiError as exc:
            last_error = exc
            if not exc.retryable or attempt == MAX_LAUNCH_ATTEMPTS:
                raise
            wait = exc.retry_after or min(DEFAULT_RETRY_WAIT_SECONDS * attempt, MAX_RETRY_WAIT_SECONDS)
            log(
                f"Retryable Cursor error on attempt {attempt}/{MAX_LAUNCH_ATTEMPTS} "
                f"(status={exc.status}): {exc}",
                error=True,
            )
            _sleep(wait, "Cursor asked us to retry")
    assert last_error is not None
    raise last_error


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
        log("Missing required env var: GITHUB_TOKEN", error=True)
        return 2
    if not cursor_api_key and not args.dry_run:
        log("Missing required env var: CURSOR_API_KEY", error=True)
        return 2

    if args.max_issues < 1:
        log("--max-issues must be >= 1", error=True)
        return 2

    try:
        issues = fetch_open_issues(args.repo, github_token, args.max_issues)
    except ApiError as exc:
        log(f"Failed fetching issues: {exc}", error=True)
        return 1

    if not issues:
        log("No open issues found.")
        return 0

    log(f"Found {len(issues)} open issue(s) to process.")
    launched = 0
    failed: list[int] = []
    last_launch_at: float | None = None

    for issue in issues:
        prompt = build_prompt(issue, args.repo, args.base_ref)
        run_name = f"Issue #{issue.number}: {issue.title[:80]}"

        if args.dry_run:
            log(f"[DRY RUN] Would launch agent for issue #{issue.number}: {issue.title}")
            launched += 1
            continue

        if last_launch_at is not None:
            elapsed = time.monotonic() - last_launch_at
            remaining = LAUNCH_SPACING_SECONDS - int(elapsed)
            if remaining > 0:
                _sleep(remaining, "avoid Cursor GitHub App rate limit between launches")

        try:
            response = create_cursor_agent_with_retry(
                cursor_api_key=cursor_api_key or "",
                model=args.model,
                repo_url=args.repo_url,
                base_ref=args.base_ref,
                prompt=prompt,
                run_name=run_name,
                skip_reviewer_request=args.skip_reviewer_request,
            )
        except ApiError as exc:
            log(f"Issue #{issue.number} launch failed: {exc}", error=True)
            failed.append(issue.number)
            last_launch_at = time.monotonic()
            continue

        last_launch_at = time.monotonic()
        log(f"Issue #{issue.number} Cursor payload keys: {sorted(response.keys())}")
        agent_id, agent_url = agent_identity(response)
        if not agent_id:
            log(
                f"Issue #{issue.number} launch returned no agent id:\n{json.dumps(response, indent=2)[:8000]}",
                error=True,
            )
            failed.append(issue.number)
            continue

        launched += 1
        log(f"Issue #{issue.number} -> agent {agent_id}")
        if agent_url:
            log(f"  URL: {agent_url}")
        run = response.get("run") if isinstance(response.get("run"), dict) else {}
        if run.get("id"):
            log(f"  Run: {run.get('id')} ({run.get('status') or 'unknown status'})")

    log(f"Launched {launched}/{len(issues)} agent(s).")
    if failed:
        failed_list = ", ".join(f"#{n}" for n in failed)
        log(f"Failed to launch agents for issues: {failed_list}", error=True)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
