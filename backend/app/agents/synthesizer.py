from app.models.state import ResearchState


def synthesize_report(state: ResearchState) -> dict[str, dict[str, object]]:
    topic = state["topic"]
    sources = state["sources"]
    return {
        "report": {
            "title": topic,
            "executive_summary": (
                f"This research brief examines {topic} through a set of established public frameworks and research resources. "
                "The evidence supports treating outcomes as context-dependent: benefits should be paired with governance, transparency, and evaluation."
            ),
            "key_findings": [
                f"{topic} is best evaluated against explicit goals, measurable outcomes, and the needs of affected stakeholders.",
                "Responsible adoption requires attention to transparency, robustness, privacy, and accountability.",
                "Current evidence and practice are evolving, so claims should be checked against primary sources and revisited over time.",
            ],
            "analysis": (
                f"The retrieved sources provide complementary perspectives on {topic}. Standards and principles help define responsible behavior, "
                "while ongoing research reports provide context for adoption and emerging trends. The main limitation of this Day-1 report is "
                "that its local adapter uses curated source summaries rather than live retrieval."
            ),
            "advantages": ["Faster access to a structured evidence map", "Repeatable research questions and source review", "Clear provenance for each retrieved source"],
            "risks": ["Curated summaries can omit recent developments", "Moderate-confidence claims still require human review", "Source selection can introduce coverage bias"],
            "conclusion": f"{topic} should be approached as an evidence-led workflow, with verification before synthesis and human judgment before publication.",
            "sources": [{"title": source["title"], "url": source["url"], "publisher": source["publisher"]} for source in sources],
        }
    }
