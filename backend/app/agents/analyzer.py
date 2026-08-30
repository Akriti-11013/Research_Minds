from app.models.state import ResearchState


def analyze_sources(state: ResearchState) -> dict[str, list[dict[str, object]]]:
    analyses = []
    for source in state["sources"]:
        analyses.append(
            {
                "source": source["title"],
                "claims": [source["snippet"]],
                "evidence_type": "framework or published research resource",
                "relevance": "high",
            }
        )
    return {"source_analysis": analyses}
