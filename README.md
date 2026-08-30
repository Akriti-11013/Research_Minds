# ResearchMind

ResearchMind is an AI-powered research synthesizer that transforms a topic into a structured research report with citations, quality checks, contradictions analysis, and Obsidian-compatible Markdown output. It combines LangGraph orchestration, FastAPI backend, and a modern frontend UI.

## Architecture

**Backend (FastAPI + LangGraph)**
- Planner: Generates focused research questions based on topic and depth
- Researcher: Fetches sources via web search or mock adapter
- Analyzer: Summarizes and extracts key findings
- Fact Checker: Validates claims and detects contradictions
- Synthesizer: Produces structured reports with citations and quality metadata
- Obsidian Export: Generates Markdown with YAML frontmatter for vault integration

**Frontend (Vite + Vanilla JS)**
- Topic input with depth control
- Configurable source count and output format
- Focus areas selection (Productivity, Security, Governance, Trends)
- Live research progress display
- Report visualization with sources, citations, and quality metrics

**Provider Abstraction**
- LLM support: OpenAI, Anthropic, or mock/local
- Search support: Tavily or mock/local adapter
- Settings-based provider switching via environment config

## Quick Start

### Backend Setup (Windows)

```powershell
cd backend
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Backend runs at `http://localhost:8000`  
API docs: `http://localhost:8000/docs`

### Frontend Setup (Windows)

```powershell
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

### Run Both Together (Recommended)

**Terminal 1 (Backend):**
```powershell
cd backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 (Frontend):**
```powershell
cd frontend
npm run dev
```

Then open `http://localhost:5173` in your browser.

## API Endpoints

**POST /api/research**
```json
{
  "topic": "Impact of Generative AI on software development",
  "depth": "standard",
  "focus_areas": ["productivity", "security"],
  "number_of_sources": 5,
  "output_format": "markdown"
}
```

Response includes:
- `report`: Structured research brief with executive summary, key findings, sources
- `markdown`: Obsidian-ready Markdown with citations and metadata
- `research_id`: Unique identifier for the research session

## Configuration

### Environment Variables (Optional)

Create `.env` in `backend/` to use real providers:

```
LLM_PROVIDER=openai         # or: anthropic, mock
SEARCH_PROVIDER=tavily      # or: mock
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=claude-...
TAVILY_API_KEY=tvly-...
```

Without these, the system runs in **local deterministic mode** and works offline.

## Testing

**Backend Tests:**
```powershell
cd backend
py -m pytest -q
```

All tests pass without API keys when using mock/local adapters.

## Build Frontend for Production

```powershell
cd frontend
npm run build
```

Outputs to `frontend/dist/` for deployment.

## Key Features

✅ Multi-stage research pipeline with quality assurance  
✅ Source attribution with URL and publisher  
✅ Contradiction detection across sources  
✅ Quality scoring and metrics  
✅ Obsidian-compatible Markdown export  
✅ Works offline with deterministic local adapters  
✅ Optional integration with OpenAI, Anthropic, Tavily  
✅ Responsive frontend UI with live progress tracking  

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── agents/          # Research pipeline stages
│   │   ├── api/             # FastAPI routes
│   │   ├── services/        # LLM and search providers
│   │   ├── models/          # Data schemas
│   │   ├── graph/           # LangGraph workflow
│   │   └── config.py        # Settings
│   ├── tests/               # Test suite
│   └── requirements.txt
├── frontend/
│   ├── main.js              # UI logic
│   ├── style.css            # Styling
│   ├── index.html           # Entry point
│   └── vite.config.js
└── README.md
```

## License

MIT
