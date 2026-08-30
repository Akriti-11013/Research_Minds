from app.config import settings
from app.models.state import ResearchState, Source
from app.services.integrations import fetch_sources_for_topic


def research_sources(state: ResearchState) -> dict[str, list[Source]]:
    topic = state["topic"]
    depth = state["depth"]
    search_enabled = settings.search_provider != "mock" and bool(settings.tavily_api_key)
    sources = fetch_sources_for_topic(topic, depth, search_enabled=search_enabled)
    return {"sources": sources}
