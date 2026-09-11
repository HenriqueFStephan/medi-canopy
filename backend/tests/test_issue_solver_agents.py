"""Tests for AI agent issue-solver trigger gating and prompts."""

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from run_issue_solver_agents import (  # noqa: E402
    CORRECTION_PREFIX,
    POST_PREFIX,
    Issue,
    IssueComment,
    build_prompt,
    comment_has_prefix,
    extract_source_links,
    skip_reason,
)


def make_issue(**overrides) -> Issue:
    defaults = {
        "number": 42,
        "title": "Fix the header",
        "body": "Change the header copy.",
        "html_url": "https://github.com/org/repo/issues/42",
        "labels": ["solve"],
    }
    defaults.update(overrides)
    return Issue(**defaults)


def make_comment(body: str, **overrides) -> IssueComment:
    defaults = {
        "id": 99,
        "body": body,
        "html_url": "https://github.com/org/repo/issues/42#issuecomment-99",
        "user": "henri",
    }
    defaults.update(overrides)
    return IssueComment(**defaults)


def test_comment_prefix_matches_start_only():
    assert comment_has_prefix("[CORRECTION] - redo the header", CORRECTION_PREFIX)
    assert comment_has_prefix("  [POST] paper DOI 10.1/xyz", POST_PREFIX)
    assert not comment_has_prefix("please [CORRECTION] later", CORRECTION_PREFIX)
    assert not comment_has_prefix("[POST] paper", CORRECTION_PREFIX)


def test_skip_reason_solve_ignores_research_digests():
    digest = make_issue(
        title="[RESEARCH] Daily Cannabis 2026-09-08",
        labels=["daily-cannabis", "research"],
    )
    assert skip_reason(digest, trigger="solve") == "label daily-cannabis"
    assert skip_reason(digest, trigger="post") is None
    assert skip_reason(digest, trigger="correction") is None


def test_skip_reason_post_requires_daily_cannabis():
    issue = make_issue(labels=["solve"])
    reason = skip_reason(issue, trigger="post")
    assert reason is not None and "daily-cannabis" in reason
    assert skip_reason(make_issue(labels=["daily-cannabis"]), trigger="post") is None


def test_skip_reason_solve_requires_solve_label():
    issue = make_issue(labels=["bug"])
    assert skip_reason(issue, trigger="solve") == "missing `solve` label"
    assert skip_reason(issue, trigger="correction") is None


def test_solve_prompt_uses_issue_as_task():
    prompt = build_prompt(make_issue(), "org/repo", "main", trigger="solve")
    assert "this labeled `solve` issue is the task" in prompt
    assert "Fix the header" in prompt
    assert "Change the header copy." in prompt
    assert "[CORRECTION]" not in prompt
    assert "[POST]" not in prompt


def test_correction_prompt_leads_with_comment():
    comment = make_comment("[CORRECTION] - redo the header changing the font")
    prompt = build_prompt(
        make_issue(),
        "org/repo",
        "main",
        trigger="correction",
        comment=comment,
    )
    assert "Apply a CORRECTION" in prompt
    assert "redo the header changing the font" in prompt
    assert "Original issue (context only)" in prompt
    assert "Change the header copy." in prompt


def test_extract_source_links_from_digest():
    body = (
        "## Medical\n"
        "- [Cannabidiol for refractory epilepsy](https://doi.org/10.1000/example)\n"
        "  - DOI: `10.1000/example`\n"
        "- Extra note https://pubmed.ncbi.nlm.nih.gov/123\n"
    )
    links = extract_source_links(body)
    assert links[0] == "https://doi.org/10.1000/example"
    assert "https://pubmed.ncbi.nlm.nih.gov/123" in links


def test_post_prompt_uses_comment_and_digest():
    comment = make_comment("[POST] Cannabidiol for refractory epilepsy")
    issue = make_issue(
        title="[RESEARCH] Daily Cannabis 2026-09-08",
        body=(
            "## Medical\n"
            "- [Cannabidiol for refractory epilepsy](https://doi.org/10.1000/example)\n"
            "  - The Lancet Neurology · 2026 · Silva et al.\n"
            "  - DOI: `10.1000/example`\n"
        ),
        labels=["daily-cannabis", "research"],
    )
    prompt = build_prompt(issue, "org/repo", "main", trigger="post", comment=comment)
    assert "Publish the named paper" in prompt
    assert "Cannabidiol for refractory epilepsy" in prompt
    assert "backend/data/seed/blog.json" in prompt
    assert "backend/data/seed/news.json" in prompt
    assert "do not close this research digest" in prompt.lower() or "do not close issue" in prompt.lower()
    assert "agent_research" in prompt
    assert "Read the paper" in prompt
    assert "https://doi.org/10.1000/example" in prompt
    assert "clickable markdown" in prompt
    assert "source_url" in prompt
    assert "Principais achados" in prompt
    assert "600–1000" in prompt
    assert "one-paragraph Resumo" in prompt
    assert "Do NOT:" in prompt
