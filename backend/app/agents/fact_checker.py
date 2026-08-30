from app.models.state import ResearchState


def check_facts(state: ResearchState) -> dict[str, list[dict[str, object]]]:
    checks = []
    for analysis in state["source_analysis"]:
        checks.append(
            {
                "claim": analysis["claims"][0],
                "status": "supported",
                "confidence": "moderate",
                "source": analysis["source"],
            }
        )
    return {"fact_checks": checks}
