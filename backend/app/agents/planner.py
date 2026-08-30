from app.config import settings
from app.models.state import ResearchState
from app.services.integrations import build_research_plan


def plan_research(state: ResearchState) -> dict[str, object]:
    topic = state["topic"]
    depth = state["depth"]
    llm_enabled = settings.llm_provider != "mock" and bool(
        settings.openai_api_key or settings.anthropic_api_key
    )
    questions = build_research_plan(topic, depth, llm_enabled=llm_enabled)
    return {
        "research_plan": questions,
        "status": "planning",
        "research_id": state.get("research_id") or "research-local",
        "focus_areas": state.get("focus_areas", []),
        "number_of_sources": state.get("number_of_sources", 5),
        "output_format": state.get("output_format", "markdown"),
    }
