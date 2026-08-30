from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from app.graph.workflow import workflow
from app.models.schemas import ResearchRequest, ResearchResponse

router = APIRouter()


@router.post("/research", response_model=ResearchResponse)
def create_research(request: ResearchRequest) -> ResearchResponse:
    from uuid import uuid4

    payload = request.model_dump(exclude_none=True)
    payload["topic"] = request.topic.strip()
    payload["research_id"] = request.research_id or f"research-{uuid4().hex[:8]}"
    result = workflow.invoke(payload)
    return ResearchResponse(
        topic=request.topic.strip(),
        depth=request.depth,
        research_id=result.get("research_id") or payload["research_id"],
        report=result["report"],
        markdown=result["markdown"],
    )


@router.post("/research/markdown", response_class=PlainTextResponse)
def create_markdown(request: ResearchRequest) -> str:
    payload = request.model_dump(exclude_none=True)
    payload["topic"] = request.topic.strip()
    result = workflow.invoke(payload)
    return result["markdown"]
