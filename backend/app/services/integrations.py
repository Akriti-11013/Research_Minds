"""Integration helpers for local and provider-backed research workflows."""

from __future__ import annotations

import asyncio

from app.config import settings
from app.services.llm import LLMClient
from app.services.search import SearchService


def _default_research_questions(topic: str, depth: str) -> list[str]:
    questions = [
        f"How is {topic} being used in practice?",
        f"What benefits and measurable outcomes are associated with {topic}?",
        f"What risks, limitations, or unintended effects should be considered?",
        f"What trends and open questions are likely to shape {topic} next?",
    ]
    if depth == "quick":
        return questions[:2]
    if depth == "deep":
        questions.append(f"Which stakeholders are most affected by {topic}?")
    return questions


def _default_sources(topic: str, depth: str) -> list[dict[str, str]]:
    sources = [
        {
            "title": "NIST AI Risk Management Framework",
            "url": "https://www.nist.gov/itl/ai-risk-management-framework",
            "publisher": "National Institute of Standards and Technology",
            "snippet": f"A voluntary framework for managing risks and improving trustworthy AI practices relevant to {topic}.",
        },
        {
            "title": "OECD AI Principles",
            "url": "https://oecd.ai/en/ai-principles",
            "publisher": "OECD.AI",
            "snippet": f"International principles covering responsible stewardship, transparency, robustness, and accountability in AI applied to {topic}.",
        },
        {
            "title": "Stanford AI Index Report",
            "url": "https://aiindex.stanford.edu/report/",
            "publisher": "Stanford Institute for Human-Centered Artificial Intelligence",
            "snippet": f"Annual evidence and trend analysis that can contextualize adoption, investment, capability, and impact related to {topic}.",
        },
    ]
    if depth == "quick":
        return sources[:2]
    return sources


def _parse_questions(raw: str) -> list[str]:
    cleaned: list[str] = []
    for line in raw.splitlines():
        item = line.strip().strip("-•*\t ")
        if not item:
            continue
        if item.lower().startswith("here are"):
            continue
        cleaned.append(item)
    return cleaned[:6]


def build_research_plan(topic: str, depth: str = "standard", llm_enabled: bool = False) -> list[str]:
    """Return a research plan, preferring an LLM provider when enabled."""
    fallback = _default_research_questions(topic, depth)
    if not llm_enabled:
        return fallback

    try:
        provider = settings.llm_provider or "mock"
        api_key = settings.openai_api_key or settings.anthropic_api_key
        model = settings.llm_model
        client = LLMClient(provider=provider, api_key=api_key, model=model)
        prompt = (
            f"Generate 3 to 5 concise, high-signal research questions about {topic}. "
            "Return one question per line with no numbering and no surrounding commentary."
        )
        generate_method = getattr(client, "generate")
        result = asyncio.run(generate_method(prompt, temperature=0.2))
        parsed = _parse_questions(result)
        if parsed:
            return parsed
    except Exception:
        pass
    return fallback


def fetch_sources_for_topic(
    topic: str,
    depth: str = "standard",
    search_enabled: bool = False,
    max_results_per_query: int = 3,
) -> list[dict[str, str]]:
    """Fetch research sources, preferring the configured search provider when enabled."""
    fallback = _default_sources(topic, depth)
    if not search_enabled:
        return fallback

    try:
        provider = settings.search_provider or "mock"
        service = SearchService(provider=provider, api_key=settings.tavily_api_key)
        queries = [topic, f"{topic} evidence", f"{topic} risks and opportunities"]
        if depth == "quick":
            queries = queries[:2]
        elif depth == "deep":
            queries = queries + [f"{topic} industry trends"]

        search_method = getattr(SearchService, "search_multiple_queries")
        sources = asyncio.run(search_method(service, queries, max_results_per_query))
        if sources:
            return sources[:max_results_per_query * 2]
    except Exception:
        pass
    return fallback
