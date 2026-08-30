from langgraph.graph import END, START, StateGraph

from app.agents.analyzer import analyze_sources
from app.agents.fact_checker import check_facts
from app.agents.obsidian import export_obsidian
from app.agents.planner import plan_research
from app.agents.researcher import research_sources
from app.agents.synthesizer import synthesize_report
from app.models.state import ResearchState


def build_workflow():
    graph = StateGraph(ResearchState)
    graph.add_node("planner", plan_research)
    graph.add_node("researcher", research_sources)
    graph.add_node("analyzer", analyze_sources)
    graph.add_node("fact_checker", check_facts)
    graph.add_node("synthesizer", synthesize_report)
    graph.add_node("obsidian_exporter", export_obsidian)
    graph.add_edge(START, "planner")
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "analyzer")
    graph.add_edge("analyzer", "fact_checker")
    graph.add_edge("fact_checker", "synthesizer")
    graph.add_edge("synthesizer", "obsidian_exporter")
    graph.add_edge("obsidian_exporter", END)
    return graph.compile()


workflow = build_workflow()
