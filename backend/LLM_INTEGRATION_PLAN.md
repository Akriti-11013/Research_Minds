# ResearchMind — LLM Integration Plan

## Current State
✅ **Mock pipeline working perfectly**
- All 6 agents execute and produce structured output
- LangGraph workflow compiles and runs end-to-end
- FastAPI backend serves requests successfully
- Obsidian markdown generation works

## What's Next: LLM-Powered Agents

### Phase 1: Add LLM Provider Support

We'll support multiple LLM providers (swap without changing code):

```python
# app/config.py enhancements
LLM_PROVIDER = "openai"  # openai | anthropic | local
LLM_MODEL = "gpt-4-turbo"  # or claude-3.5-sonnet
LLM_API_KEY = "sk-..."
```

### Phase 2: LLM-Powered Agent Implementations

#### **Planner Agent (Enhanced)**
```
Input: Research topic + depth
Process: LLM generates 5-10 focused research questions
Output: research_questions list
```

**Key insight**: Better research questions = better results. The planner should think about:
- What angles haven't been explored?
- What's controversial vs. settled?
- What predictions does industry make?

#### **Researcher Agent (Enhanced)**
```
Input: research_questions
Process: 
  1. For each question, generate search queries
  2. Perform web searches (using SerpAPI or similar)
  3. Fetch and summarize top results
Output: List of high-quality sources with snippets
```

**Implementation options**:
- **Option A**: SerpAPI (most reliable, costs $)
- **Option B**: DuckDuckGo (free, less reliable)
- **Option C**: Tavily API (AI-native, designed for this)

#### **Analyzer Agent (Enhanced)**
```
Input: Sources + snippets
Process: For each source, LLM extracts:
  - Key claims
  - Supporting statistics
  - Arguments
  - Evidence quality
  - Relevance score
Output: Structured analysis per source
```

#### **Fact Checker Agent (CRITICAL)**
```
Input: All claims from analyzer
Process: For each claim:
  1. LLM evaluates: is this supported by sources?
  2. Cross-references multiple sources
  3. Marks as: verified / partially_verified / unverified / contradicted
Output: fact_checks with confidence scores
```

**Interview opportunity**: "I added verification before synthesis so the system doesn't blindly accept retrieved information."

#### **Synthesizer Agent (Enhanced)**
```
Input: 
  - research_questions
  - analyzed_sources
  - verified_claims
Process: LLM generates comprehensive report:
  - Executive summary
  - Key findings (from verified claims only)
  - Pros/cons
  - Industry trends
  - Conclusion
Output: Structured research report
```

#### **Obsidian Exporter (No change needed)**
Already produces perfect markdown.

---

## Implementation Steps

### Step 1: Add LLM Client
```python
# app/services/llm.py
class LLMClient:
    def __init__(self, provider: str, api_key: str, model: str):
        if provider == "openai":
            self.client = OpenAI(api_key=api_key)
        elif provider == "anthropic":
            self.client = Anthropic(api_key=api_key)
    
    async def generate(self, prompt: str) -> str:
        # Call LLM with prompt
        pass
    
    async def generate_structured(self, prompt: str, schema: dict) -> dict:
        # Use function calling for structured output
        pass
```

### Step 2: Add Web Search Service
```python
# app/services/search.py
class SearchService:
    def __init__(self, provider: str = "tavily"):
        self.provider = provider
    
    async def search(self, query: str, max_results: int = 5) -> list[Source]:
        # Search and return sources
        pass
```

### Step 3: Update Each Agent
```python
# Example: Enhanced researcher agent
async def research_sources_llm(state: ResearchState) -> ResearchState:
    questions = state["research_questions"]
    
    llm = get_llm_client()
    search_service = get_search_service()
    
    all_sources = []
    for question in questions:
        # LLM generates search queries
        queries = await llm.generate_structured(
            f"Generate 3 search queries for: {question}",
            schema={"queries": ["str"]}
        )
        
        # Search each query
        for query in queries["queries"]:
            results = await search_service.search(query)
            all_sources.extend(results)
    
    state["sources"] = all_sources
    return state
```

### Step 4: Add Dependency Injection
```python
# app/services/factory.py
def get_llm_client() -> LLMClient:
    return LLMClient(
        provider=settings.llm_provider,
        api_key=settings.llm_api_key,
        model=settings.llm_model
    )

def get_search_service() -> SearchService:
    return SearchService(provider="tavily")
```

### Step 5: Update Requirements
```txt
fastapi>=0.115,<1
uvicorn[standard]>=0.30,<1
pydantic-settings>=2.6,<3
langgraph>=0.2,<1
httpx>=0.27,<1
beautifulsoup4>=4.12,<5
pytest>=8,<9

# NEW: LLM Providers
openai>=1.0,<2
anthropic>=0.28,<1

# NEW: Web Search
tavily-python>=0.3,<1

# NEW: Vector Store (optional, for RAG)
chromadb>=0.5,<1
sentence-transformers>=2.2,<3
```

---

## Demo Script (with LLM)

```
User: "Research impact of AI on software development"
   ↓
Planner: "I'll explore these angles:
  1. Productivity improvements (metrics)
  2. Security implications
  3. Developer skill requirements shift
  4. Industry adoption rates
  5. Technical debt considerations"
   ↓
Researcher: "Searching 15 queries across multiple angles..."
   ✓ Found 42 high-quality sources
   ↓
Analyzer: "Extracting insights from sources..."
   ✓ Identified 87 key claims
   ✓ Found 23 statistics
   ✓ Mapped 15 major arguments
   ↓
Fact Checker: "Verifying claims against sources..."
   ✓ 73 claims verified
   ⚠️ 12 claims partially supported
   ✗ 2 claims contradicted
   ↓
Synthesizer: "Synthesizing comprehensive report..."
   ✓ Executive summary (200 words)
   ✓ Key findings (7 items)
   ✓ Pros/cons (detailed)
   ✓ Industry trends (emerging patterns)
   ✓ Conclusion (actionable insights)
   ↓
Output: Professional Obsidian note, ready to publish
```

---

## Architecture After LLM Integration

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │              LangGraph Workflow                     │   │
│  ├────────────────────────────────────────────────────┤   │
│  │                                                    │   │
│  │  Planner → Researcher → Analyzer →               │   │
│  │  Fact Checker → Synthesizer → Obsidian           │   │
│  │                                                    │   │
│  │  Each agent has access to:                        │   │
│  │  • LLM Client (for thinking/generation)          │   │
│  │  • Search Service (for web research)             │   │
│  │  • RAG Service (for retrieval)                   │   │
│  │                                                    │   │
│  └────────────────────────────────────────────────────┘   │
│                          │                                 │
│              ┌───────────┼───────────┐                    │
│              │           │           │                    │
│         ┌────▼───┐  ┌───▼────┐  ┌──▼─────┐              │
│         │  OpenAI   │Anthropic│  │ Claude │              │
│         └──────────┘  └────────┘  └────────┘              │
│                          │                                 │
│              ┌───────────┴───────────┐                    │
│              │                       │                    │
│         ┌────▼────────┐  ┌──────────▼─────┐             │
│         │  Tavily API  │  │  ChromaDB RAG  │             │
│         └─────────────┘  └────────────────┘             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Next Actions

1. **Create `app/services/llm.py`** - LLM client abstraction
2. **Create `app/services/search.py`** - Web search service
3. **Update agents** to use LLM instead of mocks
4. **Add `.env` file** with API keys
5. **Test with real LLM** and compare outputs
6. **Optimize prompts** based on results

---

## Why This Matters for Your Interview

When they ask "Walk us through your architecture":

> "I built a research pipeline using LangGraph where each agent has a specific responsibility. The planner generates focused research questions, the researcher searches the web and retrieves sources, the analyzer extracts structured insights, and critically—the fact checker verifies claims before synthesis. This ensures quality and prevents hallucination.
> 
> The system is designed to swap LLM providers without changing agent logic, and I used structured output (function calling) to ensure the analyzer and synthesizer produce consistent JSON that downstream agents can reliably process."

This demonstrates:
- ✅ Real agentic thinking (not just chatbot)
- ✅ Quality & verification focus
- ✅ Modular architecture
- ✅ Production-ready patterns

