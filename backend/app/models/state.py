"""
ResearchState: Shared state machine for the entire research pipeline.

This state flows through all agents, each one adding information.
"""

from dataclasses import dataclass, field
from typing import Literal, Optional, TypedDict

Depth = Literal["quick", "standard", "deep"]


class Source(TypedDict):
    title: str
    url: str
    publisher: str
    snippet: str


@dataclass
class SourceAnalysis:
    """Analysis extracted from a source."""
    source_url: str
    claims: list[str] = field(default_factory=list)
    statistics: list[str] = field(default_factory=list)
    arguments: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)


@dataclass
class FactCheck:
    """Result of fact-checking a claim."""
    claim: str
    is_verified: bool
    verification_source: Optional[str] = None
    confidence: float = 0.0
    notes: str = ""


@dataclass
class ResearchReport:
    """Final structured research report."""
    executive_summary: str = ""
    key_findings: list[str] = field(default_factory=list)
    advantages: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    industry_trends: list[str] = field(default_factory=list)
    conclusion: str = ""
    sources: list[dict] = field(default_factory=list)


class ResearchState(TypedDict, total=False):
    """
    Main state container for the entire research workflow.
    
    Each agent in the pipeline reads from this state and adds/modifies fields.
    """
    
    # Input
    topic: str
    depth: Depth
    
    # Planner Agent Output
    research_questions: list[str]
    research_plan: list[str]
    
    # Researcher Agent Output
    sources: list[Source]
    
    # Analyzer Agent Output
    source_analysis: list[dict]
    
    # Fact Checker Agent Output
    fact_checks: list[dict]
    verified_claims: list[str]
    
    # Synthesizer Agent Output
    report: dict
    
    # Obsidian Exporter Output
    markdown: str
    
    # Metadata
    status: str
    error: Optional[str]
