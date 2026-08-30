from app.config import settings
from app.services.integrations import build_research_plan, fetch_sources_for_topic
from app.services.llm import LLMClient
from app.services.search import SearchService


def test_build_research_plan_uses_provider_when_available(monkeypatch) -> None:
    async def fake_generate(self, prompt: str, temperature: float = 0.7) -> str:
        return "Question 1\nQuestion 2\nQuestion 3"

    monkeypatch.setattr(settings, "llm_provider", "openai")
    monkeypatch.setattr(settings, "openai_api_key", "test-key")
    monkeypatch.setattr(LLMClient, "generate", fake_generate)

    plan = build_research_plan("AI safety", "quick", llm_enabled=True)

    assert plan == ["Question 1", "Question 2", "Question 3"]


def test_fetch_sources_for_topic_uses_search_provider(monkeypatch) -> None:
    async def fake_search_multiple_queries(self, queries, max_results_per_query=3):
        return [
            {
                "title": "Live Source",
                "url": "https://example.com/live",
                "publisher": "Example Labs",
                "snippet": "Live search result for AI safety.",
            }
        ]

    monkeypatch.setattr(settings, "search_provider", "tavily")
    monkeypatch.setattr(settings, "tavily_api_key", "test-key")
    monkeypatch.setattr(SearchService, "search_multiple_queries", fake_search_multiple_queries)

    sources = fetch_sources_for_topic("AI safety", "standard", search_enabled=True)

    assert len(sources) == 1
    assert sources[0]["title"] == "Live Source"
