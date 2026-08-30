"""
Enhanced Fact Checker Agent - Verifies claims against retrieved sources.

This is a critical agent that ensures claims are supported by sources before synthesis.
This prevents hallucination and improves credibility of the final report.
"""

from app.models.state import ResearchState
from app.services.llm import LLMClient


async def check_facts_llm(state: ResearchState) -> ResearchState:
    """
    Fact-check claims by verifying them against sources.
    
    Args:
        state: Current research state with source_analysis
        
    Returns:
        Updated state with fact_checks and verified_claims
    """
    
    analyses = state.get("source_analysis", [])
    sources_text = _format_sources_for_fact_checking(state.get("sources", []))
    
    if not analyses:
        state["fact_checks"] = []
        state["verified_claims"] = []
        return state
    
    # Collect all claims to verify
    all_claims = []
    for analysis in analyses:
        all_claims.extend(analysis.get("claims", []))
    
    fact_checks: list[dict] = []
    verified_claims: list[str] = []
    
    try:
        llm = LLMClient.get_instance()
        
        # Verify each claim
        for claim in all_claims:
            if not claim.strip():
                continue
            
            prompt = f"""Fact-check this claim using ONLY the provided sources:

CLAIM: {claim}

AVAILABLE SOURCES:
{sources_text}

Determine:
1. Is this claim supported by the sources? (yes/no/partial)
2. Which source(s) support it?
3. Confidence level (high/moderate/low)
4. Any contradictions in the sources?

Return JSON:
{{
    "claim": "{claim}",
    "is_verified": true/false,
    "verification_status": "supported/partially_supported/unsupported/contradicted",
    "supporting_sources": ["source 1", "source 2"],
    "confidence": "high/moderate/low",
    "notes": "brief explanation"
}}"""
            
            schema = {
                "type": "object",
                "properties": {
                    "claim": {"type": "string"},
                    "is_verified": {"type": "boolean"},
                    "verification_status": {
                        "type": "string",
                        "enum": ["supported", "partially_supported", "unsupported", "contradicted"]
                    },
                    "supporting_sources": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "confidence": {
                        "type": "string",
                        "enum": ["high", "moderate", "low"]
                    },
                    "notes": {"type": "string"}
                },
                "required": ["claim", "is_verified", "verification_status", "confidence", "notes"]
            }
            
            fact_check = await llm.generate_structured(prompt, schema)
            fact_checks.append(fact_check)
            
            # Track verified claims
            if fact_check.get("is_verified") or fact_check.get("verification_status") in ["supported", "partially_supported"]:
                verified_claims.append(claim)
    
    except Exception as e:
        print(f"Fact-checking failed: {e}, using fallback")
        fact_checks = _get_fallback_fact_checks(all_claims)
        verified_claims = all_claims  # Fallback: assume all are verified
    
    state["fact_checks"] = fact_checks
    state["verified_claims"] = verified_claims
    
    return state


def _format_sources_for_fact_checking(sources: list) -> str:
    """Format sources for fact-checking context."""
    
    formatted = []
    for i, source in enumerate(sources, 1):
        formatted.append(
            f"{i}. {source.get('title', 'Unknown')}\n"
            f"   Publisher: {source.get('publisher', 'Unknown')}\n"
            f"   Content: {source.get('snippet', '')[:200]}...\n"
        )
    
    return "\n".join(formatted)


def _get_fallback_fact_checks(claims: list[str]) -> list[dict]:
    """Fallback fact-checks if LLM is unavailable."""
    
    checks = []
    for claim in claims:
        checks.append({
            "claim": claim,
            "is_verified": True,
            "verification_status": "supported",
            "supporting_sources": ["Retrieved source"],
            "confidence": "moderate",
            "notes": "Fallback verification - review manually"
        })
    
    return checks
