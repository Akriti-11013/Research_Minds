from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_research_endpoint_returns_report_and_markdown() -> None:
    response = client.post(
        "/api/research",
        json={"topic": "Impact of Generative AI on software development", "depth": "standard"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["report"]["title"] == "Impact of Generative AI on software development"
    assert body["markdown"].startswith("---\ntitle:")


def test_research_rejects_short_topics() -> None:
    response = client.post("/api/research", json={"topic": "AI", "depth": "quick"})
    assert response.status_code == 422
