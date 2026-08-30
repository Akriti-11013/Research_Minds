from app.models.state import ResearchState


def check_facts(state: ResearchState) -> dict[str, object]:
    checks = []
    contradictions = []
    for analysis in state["source_analysis"]:
        claim = analysis["claims"][0]
        checks.append(
            {
                "claim": claim,
                "status": "supported",
                "confidence": "moderate",
                "source": analysis["source"],
            }
        )

    if len(checks) > 1 and any(check["source"] != checks[0]["source"] for check in checks[1:]):
        contradictions.append(
            "Multiple sources point to different levels of evidence strength, so conclusions should be interpreted contextually."
        )

    return {
        "fact_checks": checks,
        "contradictions": contradictions,
        "verified_claims": [check["claim"] for check in checks],
        "status": "fact-checking",
    }
