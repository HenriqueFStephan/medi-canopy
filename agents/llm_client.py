"""
LLM client abstraction — placeholder until API keys are configured.

Set LLM_PROVIDER in debt.txt to openai | anthropic | placeholder.
"""

import os
from typing import Any


class LLMClient:
    """Unified interface for agent reasoning and summarization."""

    def __init__(self) -> None:
        self.provider = os.getenv("LLM_PROVIDER", "placeholder")
        self.model = os.getenv("LLM_MODEL", "gpt-4o")

    def is_placeholder(self) -> bool:
        return self.provider == "placeholder" or not os.getenv("OPENAI_API_KEY")

    def search_news(self, topics: list[str], regions: list[str]) -> list[dict[str, Any]]:
        """
        Search and synthesize news items.

        PLACEHOLDER: returns fixture data. Production: web search + LLM synthesis.
        """
        if self.is_placeholder():
            import json
            from pathlib import Path

            fixture = Path(__file__).parent / "fixtures" / "news_sample.json"
            return json.loads(fixture.read_text(encoding="utf-8"))
        # Future: OpenAI/Anthropic with web browsing or news API tools
        raise NotImplementedError("Configure LLM_PROVIDER and API keys in debt.txt")

    def fetch_papers(self, queries: list[dict]) -> list[dict[str, Any]]:
        """Fetch scholarly papers — placeholder uses fixtures."""
        if self.is_placeholder():
            import json
            from pathlib import Path

            fixture = Path(__file__).parent / "fixtures" / "papers_sample.json"
            return json.loads(fixture.read_text(encoding="utf-8"))
        raise NotImplementedError("Wire Semantic Scholar / PubMed / OpenAlex clients")

    def summarize_pt(self, text: str) -> str:
        """Portuguese summary for blog posts."""
        if self.is_placeholder():
            return ""
        raise NotImplementedError("LLM summarization not configured")
