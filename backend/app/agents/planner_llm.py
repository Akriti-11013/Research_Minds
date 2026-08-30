"""
Enhanced Planner Agent - Uses LLM to generate focused research questions.

Generates 5-10 research questions based on the topic and research depth.
"""

from app.models.state import ResearchState
from app.services.llm import LLMClient
from app.config import settings


async def plan_research_llm(state: ResearchState) -> ResearchState:
    """
    Plan research by generating focused research questions using LLM.
    
    Args:
        state: Current research state with topic
        
    Returns:
        Updated state with research_questions and research_plan
    """
    
    topic = state["topic"]
    depth = state.get("depth", "standard")
    
    # Determine number of questions based on depth
    num_questions = {
        "quick": 3,
        "standard": 5,
        "deep": 8
    }.get(depth, 5)
    
    try:
        # Try to use LLM if available
        llm = LLMClient.get_instance()
        
        # Create prompt for question generation
        prompt = f"""You are a research strategist. Generate exactly {num_questions} focused, 
specific research questions about:

Topic: {topic}
Research Depth: {depth}

Requirements:
1. Questions should be specific and answerable through research
2. Mix different angles (definition, impact, trends, challenges, future)
3. Avoid yes/no questions - use "how", "what", "why", "which"
4. Each question should guide finding different sources
5. Progress from foundational to advanced

Return ONLY the questions as a JSON list with no other text.
Example format: {{"questions": ["Question 1?", "Question 2?", ...]}}"""
        
        schema = {
            "type": "object",
            "properties": {
                "questions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of research questions"
                }
            },
            "required": ["questions"]
        }
        
        result = await llm.generate_structured(prompt, schema)
        questions = result.get("questions", _get_fallback_questions(topic, depth))
        
    except Exception as e:
        print(f"LLM generation failed: {e}, using fallback")
        questions = _get_fallback_questions(topic, depth)
    
    # Create research plan
    plan = _create_research_plan(topic, questions, depth)
    
    state["status"] = "planning"
    state["research_questions"] = questions
    state["research_plan"] = plan
    
    return state


def _get_fallback_questions(topic: str, depth: str) -> list[str]:
    """Fallback questions if LLM is not available."""
    
    base_questions = [
        f"What is the current state and definition of {topic}?",
        f"What are the main benefits and positive impacts of {topic}?",
        f"What are the key challenges and risks associated with {topic}?",
        f"How is {topic} being adopted across industries?",
        f"What are the emerging trends and future predictions for {topic}?",
    ]
    
    if depth == "quick":
        return base_questions[:3]
    elif depth == "deep":
        return base_questions + [
            f"What are the technical/implementation details of {topic}?",
            f"Who are the key players and researchers in {topic}?",
            f"What ethical or societal implications does {topic} have?",
        ]
    else:  # standard
        return base_questions


def _create_research_plan(topic: str, questions: list[str], depth: str) -> list[str]:
    """Create a structured research plan."""
    
    sources_per_question = {
        "quick": 2,
        "standard": 3,
        "deep": 5,
    }.get(depth, 3)
    
    plan = [
        f"📋 Research Plan for: {topic}",
        f"📊 Depth: {depth.upper()}",
        f"🔍 Will research {len(questions)} key questions",
        f"🌐 Target: ~{len(questions) * sources_per_question} quality sources",
        "",
        "Questions to answer:",
    ]
    
    for i, q in enumerate(questions, 1):
        plan.append(f"  {i}. {q}")
    
    return plan
