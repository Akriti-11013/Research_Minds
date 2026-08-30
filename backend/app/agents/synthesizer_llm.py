"""
Enhanced Synthesizer Agent - Uses LLM to synthesize final research report.

Combines verified claims, insights, and analysis into a comprehensive report.
"""

from app.models.state import ResearchState
from app.services.llm import LLMClient


async def synthesize_report_llm(state: ResearchState) -> ResearchState:
    """
    Synthesize a comprehensive research report from verified claims and analysis.
    
    Args:
        state: Current research state with verified_claims and analyses
        
    Returns:
        Updated state with structured report
    """
    
    topic = state.get("topic", "Research Topic")
    verified_claims = state.get("verified_claims", [])
    analyses = state.get("source_analysis", [])
    sources = state.get("sources", [])
    
    try:
        llm = LLMClient.get_instance()
        
        # Create comprehensive synthesis prompt
        claims_text = "\n".join([f"- {claim}" for claim in verified_claims[:10]])  # Limit to 10
        analyses_text = _format_analyses_for_synthesis(analyses)
        sources_text = _format_sources_for_synthesis(sources)
        
        prompt = f"""You are a research synthesizer. Create a comprehensive research report about:

TOPIC: {topic}

VERIFIED CLAIMS:
{claims_text}

SOURCE INSIGHTS:
{analyses_text}

SOURCES:
{sources_text}

Generate a structured research report with these sections:
1. Executive Summary (150-200 words)
2. Key Findings (5-7 bullet points)
3. Advantages/Benefits (4-6 points)
4. Risks/Challenges (4-6 points)
5. Conclusion (100-150 words)

Return as JSON:
{{
    "title": "{topic}",
    "executive_summary": "...",
    "key_findings": ["finding 1", "finding 2", ...],
    "advantages": ["advantage 1", ...],
    "risks": ["risk 1", ...],
    "conclusion": "..."
}}"""
        
        schema = {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "executive_summary": {"type": "string"},
                "key_findings": {"type": "array", "items": {"type": "string"}},
                "advantages": {"type": "array", "items": {"type": "string"}},
                "risks": {"type": "array", "items": {"type": "string"}},
                "conclusion": {"type": "string"}
            },
            "required": ["title", "executive_summary", "key_findings", "advantages", "risks", "conclusion"]
        }
        
        report_data = await llm.generate_structured(prompt, schema)
        
        # Add sources to report
        report_data["sources"] = [
            {
                "title": source.get("title", "Unknown"),
                "url": source.get("url", ""),
                "publisher": source.get("publisher", "Unknown")
            }
            for source in sources
        ]
        
        state["report"] = report_data
    
    except Exception as e:
        print(f"Synthesis failed: {e}, using fallback")
        state["report"] = _get_fallback_report(topic, verified_claims, sources)
    
    return state


def _format_analyses_for_synthesis(analyses: list[dict]) -> str:
    """Format analyses for synthesis context."""
    
    formatted = []
    for analysis in analyses[:5]:  # Limit to top 5
        formatted.append(
            f"From '{analysis.get('source', 'Unknown')}':\n"
            f"  Claims: {', '.join(analysis.get('claims', [])[:2])}\n"
            f"  Evidence: {analysis.get('evidence_type', 'unknown')}\n"
        )
    
    return "\n".join(formatted)


def _format_sources_for_synthesis(sources: list[dict]) -> str:
    """Format sources for synthesis context."""
    
    formatted = []
    for source in sources[:5]:
        formatted.append(
            f"- {source.get('title', 'Unknown')}\n"
            f"  {source.get('publisher', 'Unknown')}"
        )
    
    return "\n".join(formatted)


def _get_fallback_report(topic: str, claims: list[str], sources: list[dict]) -> dict:
    """Fallback report if LLM is unavailable."""
    
    return {
        "title": topic,
        "executive_summary": (
            f"This research brief examines {topic} through verified sources and analysis. "
            "The evidence supports a comprehensive understanding of the topic with consideration "
            "for both benefits and challenges."
        ),
        "key_findings": claims[:5] if claims else [
            f"{topic} is complex and multifaceted",
            "Multiple perspectives should be considered",
            "Evidence is evolving and context-dependent"
        ],
        "advantages": [
            "Verified research supports key claims",
            "Multiple sources provide diverse perspectives",
            "Clear evidence path documented"
        ],
        "risks": [
            "Rapid evolution of field requires ongoing review",
            "Some claims may be partially supported",
            "Context-dependent findings require interpretation"
        ],
        "conclusion": f"{topic} should be approached with evidence-led methodology and regular review.",
        "sources": [
            {
                "title": source.get("title", "Unknown"),
                "url": source.get("url", ""),
                "publisher": source.get("publisher", "Unknown")
            }
            for source in sources
        ]
    }
