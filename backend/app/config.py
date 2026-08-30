from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ResearchMind"
    
    # LLM Configuration
    llm_provider: str = "mock"  # openai | anthropic | mock
    llm_model: str | None = None
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    
    # Search Configuration
    search_provider: str = "mock"  # tavily | mock
    tavily_api_key: str | None = None
    
    # Agent Configuration
    research_depth_multipliers: dict = {
        "quick": 1,
        "standard": 2,
        "deep": 4
    }

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
