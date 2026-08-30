from typing import Literal

from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    topic: str = Field(min_length=3, max_length=500)
    depth: Literal["quick", "standard", "deep"] = "standard"


class ResearchResponse(BaseModel):
    topic: str
    depth: str
    report: dict[str, object]
    markdown: str
