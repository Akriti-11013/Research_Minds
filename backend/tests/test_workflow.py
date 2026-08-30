from app.graph.workflow import workflow


def test_workflow_creates_obsidian_note() -> None:
    result = workflow.invoke({"topic": "Impact of Generative AI on software development", "depth": "standard"})

    assert result["report"]["title"] == "Impact of Generative AI on software development"
    assert len(result["sources"]) == 3
    assert len(result["fact_checks"]) == 3
    assert result["markdown"].startswith("---\ntitle:")
    assert "## Key Findings" in result["markdown"]
    assert "## Sources" in result["markdown"]


def test_quick_depth_reduces_research_scope() -> None:
    result = workflow.invoke({"topic": "AI safety", "depth": "quick"})

    assert len(result["research_plan"]) == 2
    assert len(result["sources"]) == 2
