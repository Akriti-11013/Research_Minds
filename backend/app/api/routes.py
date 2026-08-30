from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from app.graph.workflow import workflow
from app.models.schemas import ResearchRequest, ResearchResponse

router = APIRouter()


@router.post("/research", response_model=ResearchResponse)
def create_research(request: ResearchRequest) -> ResearchResponse:
    result = workflow.invoke({"topic": request.topic.strip(), "depth": request.depth})
    return ResearchResponse(
        topic=request.topic.strip(),
        depth=request.depth,
        report=result["report"],
        markdown=result["markdown"],
    )


@router.post("/research/markdown", response_class=PlainTextResponse)
def create_markdown(request: ResearchRequest) -> str:
    result = workflow.invoke({"topic": request.topic.strip(), "depth": request.depth})
    return result["markdown"]
