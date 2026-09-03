"""Tests for the daily cannabis research digest helpers."""

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import pytest  # noqa: E402

import run_daily_cannabis_research as daily  # noqa: E402
from run_daily_cannabis_research import (  # noqa: E402
    DEFAULT_ISSUE_LABELS,
    Paper,
    build_prompt,
    extract_json_payload,
    filter_reliable_papers,
    issue_title,
    parse_papers,
    publish_issue,
    rejection_reason,
    render_issue_body,
    render_summary,
)

MIN_CONFIDENCE = 0.7


def make_paper(**overrides) -> Paper:
    defaults = {
        "title": "Cannabidiol for refractory epilepsy: a randomized trial",
        "url": "https://doi.org/10.1000/example",
        "journal": "The Lancet Neurology",
        "authors": "Silva et al.",
        "year": 2026,
        "doi": "10.1000/example",
        "category": "medical",
        "publication_type": "journal-article",
        "peer_reviewed": True,
        "confidence": 0.92,
        "summary": "Reduced seizure frequency versus placebo.",
    }
    defaults.update(overrides)
    return Paper(**defaults)


def test_extract_json_payload_from_fenced_block():
    text = 'Here you go:\n\n```json\n{"papers": [{"title": "A"}]}\n```\n\nDone.'
    assert extract_json_payload(text) == {"papers": [{"title": "A"}]}


def test_extract_json_payload_without_fence():
    text = 'Result: {"papers": []} end'
    assert extract_json_payload(text) == {"papers": []}


def test_extract_json_payload_rejects_empty_result():
    with pytest.raises(ValueError):
        extract_json_payload("   ")


def test_parse_papers_normalizes_doi_and_confidence():
    payload = {
        "papers": [
            {
                "title": "Hempcrete thermal performance",
                "url": "https://www.sciencedirect.com/science/article/pii/S000",
                "journal": "Construction and Building Materials",
                "doi": "https://doi.org/10.1016/j.example",
                "year": "2026-03",
                "confidence": 88,
                "peer_reviewed": True,
            }
        ]
    }
    papers = parse_papers(payload)
    assert papers[0].doi == "10.1016/j.example"
    assert papers[0].year == 2026
    assert papers[0].confidence == pytest.approx(0.88)


def test_parse_papers_requires_papers_list():
    with pytest.raises(ValueError):
        parse_papers({"results": []})


def test_reliable_paper_is_accepted():
    assert rejection_reason(make_paper(), MIN_CONFIDENCE) is None


@pytest.mark.parametrize(
    "overrides, expected_fragment",
    [
        ({"peer_reviewed": False}, "peer-reviewed"),
        ({"publication_type": "preprint"}, "not peer-reviewed"),
        ({"url": "https://www.biorxiv.org/content/10.1101/2026.01.01"}, "preprint"),
        ({"journal": ""}, "journal"),
        ({"title": ""}, "title"),
        ({"url": ""}, "missing link"),
        ({"confidence": 0.4}, "below threshold"),
        ({"doi": "", "url": "https://some-cannabis-blog.example.com/post"}, "not a recognised"),
    ],
)
def test_unreliable_papers_are_rejected(overrides, expected_fragment):
    reason = rejection_reason(make_paper(**overrides), MIN_CONFIDENCE)
    assert reason is not None
    assert expected_fragment in reason


def test_paper_without_doi_but_scholarly_host_is_accepted():
    paper = make_paper(doi="", url="https://pubmed.ncbi.nlm.nih.gov/12345678/")
    assert rejection_reason(paper, MIN_CONFIDENCE) is None


def test_filter_deduplicates_by_doi_and_sorts_by_confidence():
    papers = [
        make_paper(title="Lower confidence", doi="10.1000/a", url="https://doi.org/10.1000/a", confidence=0.75),
        make_paper(title="Higher confidence", doi="10.1000/b", url="https://doi.org/10.1000/b", confidence=0.95),
        make_paper(title="Duplicate", doi="10.1000/A", url="https://doi.org/10.1000/a", confidence=0.9),
    ]
    outcome = filter_reliable_papers(papers, MIN_CONFIDENCE)

    assert [p.title for p in outcome.accepted] == ["Higher confidence", "Lower confidence"]
    assert outcome.rejected[0][1] == "duplicate of an earlier entry"


def test_render_summary_includes_title_and_links():
    outcome = filter_reliable_papers([make_paper()], MIN_CONFIDENCE)
    summary = render_summary("2026-09-03", outcome)

    assert summary.startswith("# Daily Cannabis 2026-09-03")
    assert "https://doi.org/10.1000/example" in summary
    assert "Medical" in summary


def test_render_summary_handles_no_reliable_papers():
    outcome = filter_reliable_papers([make_paper(peer_reviewed=False)], MIN_CONFIDENCE)
    summary = render_summary("2026-09-03", outcome)

    assert "No peer-reviewed papers cleared the reliability checks today." in summary
    assert "Discarded as unreliable (1)" in summary


def test_prompt_covers_required_domains():
    prompt = build_prompt("2026-09-03", 12, MIN_CONFIDENCE)

    assert "Daily Cannabis 2026-09-03" in prompt
    for keyword in ("Medical", "fashion and textiles", "construction", "peer-reviewed"):
        assert keyword in prompt


def test_issue_title_matches_requested_format():
    assert issue_title("2026-09-03") == "Daily Cannabis 2026-09-03"


def test_issue_body_lists_reliable_links_without_discarded_ones():
    papers = [make_paper(), make_paper(title="Sketchy claim", peer_reviewed=False, doi="10.1000/x")]
    outcome = filter_reliable_papers(papers, MIN_CONFIDENCE)

    body = render_issue_body("2026-09-03", outcome)

    assert "https://doi.org/10.1000/example" in body
    assert "1 further candidate was discarded" in body
    # The unreliable entry must never be linked or named in the issue.
    assert "Sketchy claim" not in body


def test_publish_issue_creates_issue_with_labels(monkeypatch):
    captured = {}

    monkeypatch.setattr(daily, "find_issue_by_title", lambda *a, **k: None)

    def fake_create(repo, token, *, title, body, labels):
        captured.update(repo=repo, token=token, title=title, body=body, labels=labels)
        return {"html_url": "https://github.com/org/repo/issues/9"}

    monkeypatch.setattr(daily, "create_github_issue", fake_create)

    outcome = filter_reliable_papers([make_paper()], MIN_CONFIDENCE)
    url = publish_issue(
        repo="org/repo",
        github_token="t0ken",
        date_str="2026-09-03",
        outcome=outcome,
        labels=list(DEFAULT_ISSUE_LABELS),
    )

    assert url == "https://github.com/org/repo/issues/9"
    assert captured["title"] == "Daily Cannabis 2026-09-03"
    assert "daily-cannabis" in captured["labels"]
    assert "https://doi.org/10.1000/example" in captured["body"]


def test_publish_issue_is_idempotent_for_the_same_day(monkeypatch):
    monkeypatch.setattr(
        daily,
        "find_issue_by_title",
        lambda *a, **k: {"html_url": "https://github.com/org/repo/issues/5"},
    )

    def fail_create(*args, **kwargs):
        raise AssertionError("must not create a duplicate issue")

    monkeypatch.setattr(daily, "create_github_issue", fail_create)

    outcome = filter_reliable_papers([make_paper()], MIN_CONFIDENCE)
    url = publish_issue(
        repo="org/repo",
        github_token="t0ken",
        date_str="2026-09-03",
        outcome=outcome,
        labels=list(DEFAULT_ISSUE_LABELS),
    )

    assert url == "https://github.com/org/repo/issues/5"
