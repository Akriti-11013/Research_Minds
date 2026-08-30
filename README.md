# ResearchMind

ResearchMind is an AI research synthesizer that turns a topic into a structured report and an Obsidian-compatible Markdown note.

## Day-1 backend

The backend uses FastAPI and LangGraph. It runs with a deterministic local research adapter, so the full workflow works without API keys. The adapter boundary is in `backend/app/agents/researcher.py` and can later be replaced by a web search and LLM provider.

### Run on Windows

```powershell
cd backend
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API.

### Example request

```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:8000/api/research -ContentType 'application/json' -Body '{"topic":"Impact of Generative AI on software development","depth":"standard"}'
```

The response contains `report` and `markdown`. The Markdown includes YAML frontmatter and can be saved directly into an Obsidian vault.

### Test

```powershell
cd backend
py -m pytest
```
