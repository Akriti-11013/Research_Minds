"""
Enhanced Researcher Agent - Uses web search to find relevant sources.

Searches for sources matching each research question and returns high-quality results.
"""

import asyncio
from app.models.state import ResearchState, Source
from app.services.search import SearchService
from app.config import settings


async def research_sources_llm(state: ResearchState) -> ResearchState:
    """
    Research by searching for sources for each research question.
    
    Args:
        state: Current research state with research_questions
        
    Returns:
        Updated state with sources
    """
    
    questions = state.get("research_questions", [])
    depth = state.get("depth", "standard")
    
    if not questions:
        state["sources"] = []
        return state
    
    # Determine search depth
    max_results_per_question = {
        "quick": 2,
        "standard": 3,
        "deep": 5,
    }.get(depth, 3)
    
    try:
        # Initialize search service
        search_service = SearchService(
            provider=settings.search_provider,
            api_key=settings.tavily_api_key
        )
        
        # Search for each question
        all_sources: list[Source] = []
        seen_urls = set()
        
        for question in questions:
            # Perform search
            results = await search_service.search(
                query=question,
                max_results=max_results_per_question
            )
            
            # Deduplicate by URL
            for source in results:
                url = source["url"]
                if url not in seen_urls:
                    all_sources.append(source)
                    seen_urls.add(url)
        
        state["sources"] = all_sources
        
    except Exception as e:
        print(f"Search error: {e}, using fallback sources")
        state["sources"] = _get_fallback_sources(state["topic"])
    
    return state


def _get_fallback_sources(topic: str) -> list[Source]:
    """Fallback sources if search is unavailable."""
    
    return [
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
