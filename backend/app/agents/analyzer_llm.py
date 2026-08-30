"""
Enhanced Analyzer Agent - Uses LLM to extract insights from sources.

Extracts claims, statistics, arguments, and evidence from each source.
"""

from app.models.state import ResearchState
from app.services.llm import LLMClient


async def analyze_sources_llm(state: ResearchState) -> ResearchState:
    """
    Analyze sources by extracting structured insights using LLM.
    
    Args:
        state: Current research state with sources
        
    Returns:
        Updated state with source_analysis
    """
    
    sources = state.get("sources", [])
    
    if not sources:
        state["source_analysis"] = []
        return state
    
    analyses: list[dict] = []
    
    try:
        llm = LLMClient.get_instance()
        
        for source in sources:
            prompt = f"""Analyze this research source and extract structured insights:

Title: {source.get('title', 'Unknown')}
Source: {source.get('publisher', 'Unknown')}
Content: {source.get('snippet', '')}

Extract:
1. Key claims (factual statements)
2. Statistics (numbers, metrics, data)
3. Arguments (reasoning, explanations)
4. Evidence quality (strong/moderate/weak)

Return as JSON with this structure:
{{
    "claims": ["claim 1", "claim 2", ...],
    "statistics": ["stat 1", "stat 2", ...],
    "arguments": ["arg 1", "arg 2", ...],
    "evidence_type": "framework/research/industry/other",
    "relevance": "high/medium/low"
}}"""
            
            schema = {
                "type": "object",
                "properties": {
                    "claims": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "statistics": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "arguments": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "evidence_type": {
                        "type": "string",
                        "enum": ["framework", "research", "industry", "other"]
                    },
                    "relevance": {
                        "type": "string",
                        "enum": ["high", "medium", "low"]
                    }
                },
                "required": ["claims", "statistics", "arguments", "evidence_type", "relevance"]
            }
            
            analysis = await llm.generate_structured(prompt, schema)
            
            # Add source info
            analysis["source"] = source.get("title", "Unknown")
            analysis["url"] = source.get("url", "")
            
            analyses.append(analysis)
    
    except Exception as e:
        print(f"LLM analysis failed: {e}, using fallback")
        analyses = _get_fallback_analyses(sources)
    
    state["source_analysis"] = analyses
    return state


def _get_fallback_analyses(sources: list) -> list[dict]:
    """Fallback analysis if LLM is unavailable."""
    
    analyses = []
    for source in sources:
        analyses.append({
            "source": source.get("title", "Unknown"),
            "url": source.get("url", ""),
            "claims": [source.get("snippet", "")],
            "statistics": [],
            "arguments": [],
            "evidence_type": "framework",
            "relevance": "high",
        })
    
    return analyses
