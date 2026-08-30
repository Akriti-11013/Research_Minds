from typing import Literal

from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    topic: str = Field(min_length=3, max_length=500)
    depth: Literal["quick", "standard", "deep"] = "standard"
    research_id: str | None = None
    focus_areas: list[str] = Field(default_factory=list)
    number_of_sources: int = Field(default=5, ge=1, le=20)
    output_format: Literal["markdown", "json"] = "markdown"


class ResearchResponse(BaseModel):
    topic: str
    depth: str
    research_id: str | None = None
    report: dict[str, object]
    markdown: str
