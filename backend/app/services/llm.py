"""
LLM Client - Abstracts different LLM providers (OpenAI, Anthropic, etc.)

This allows swapping providers without changing agent code.
"""

import os
from typing import Optional, Any
import json
from abc import ABC, abstractmethod

from app.config import settings


class LLMProvider(ABC):
    """Abstract base for LLM providers."""
    
    @abstractmethod
    async def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate text from a prompt."""
        pass
    
    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        schema: dict,
        temperature: float = 0.1
    ) -> dict:
        """Generate structured output (JSON) from a prompt."""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI GPT models."""
    
    def __init__(self, api_key: str, model: str = "gpt-4-turbo"):
        try:
            from openai import AsyncOpenAI
        except ImportError:
            raise ImportError(
                "openai not installed. Install with: pip install openai"
            )
        
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
    
    async def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate text using OpenAI."""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return response.choices[0].message.content
    
    async def generate_structured(
        self,
        prompt: str,
        schema: dict,
        temperature: float = 0.1
    ) -> dict:
        """Generate structured JSON output using function calling."""
        from openai import AsyncOpenAI
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            functions=[
                {
                    "name": "return_structured_output",
                    "description": "Return structured output",
                    "parameters": schema
                }
            ],
            function_call={"name": "return_structured_output"},
        )
        
        # Extract the function call arguments
        if response.choices[0].message.function_call:
            return json.loads(
                response.choices[0].message.function_call.arguments
            )
        return {}


class AnthropicProvider(LLMProvider):
    """Anthropic Claude models."""
    
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        try:
            from anthropic import AsyncAnthropic
        except ImportError:
            raise ImportError(
                "anthropic not installed. Install with: pip install anthropic"
            )
        
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = model
    
    async def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate text using Claude."""
        message = await self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return message.content[0].text
    
    async def generate_structured(
        self,
        prompt: str,
        schema: dict,
        temperature: float = 0.1
    ) -> dict:
        """Generate structured JSON output."""
        # Add JSON format instruction to prompt
        json_prompt = (
            f"{prompt}\n\n"
            "Please respond with ONLY valid JSON in this format:\n"
            f"{json.dumps(schema, indent=2)}\n\n"
            "Do not include any other text."
        )
        
        message = await self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[{"role": "user", "content": json_prompt}],
            temperature=temperature,
        )
        
        try:
            return json.loads(message.content[0].text)
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract JSON from response
            text = message.content[0].text
            try:
                start = text.find('{')
                end = text.rfind('}') + 1
                if start >= 0 and end > start:
                    return json.loads(text[start:end])
            except json.JSONDecodeError:
                pass
            return {}


class MockProvider(LLMProvider):
    """Mock provider for testing without API calls."""
    
    async def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Return mock response."""
        return f"Mock response to: {prompt[:50]}..."
    
    async def generate_structured(
        self,
        prompt: str,
        schema: dict,
        temperature: float = 0.1
    ) -> dict:
        """Return mock structured response."""
        # Return a dict matching the schema structure
        return {key: [] for key in schema.get("properties", {}).keys()}


class LLMClient:
    """Unified LLM client that can use different providers."""
    
    _instance: Optional["LLMClient"] = None
    
    def __init__(
        self,
        provider: str = "openai",
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.provider_name = provider
        
        # Get API key from parameter or settings
        if provider == "openai":
            api_key = api_key or settings.openai_api_key
            model = model or "gpt-4-turbo"
            if not api_key:
                raise ValueError("OpenAI API key not found")
            self.provider = OpenAIProvider(api_key, model)
        
        elif provider == "anthropic":
            api_key = api_key or settings.anthropic_api_key
            model = model or "claude-3-5-sonnet-20241022"
            if not api_key:
                raise ValueError("Anthropic API key not found")
            self.provider = AnthropicProvider(api_key, model)
        
        elif provider == "mock":
            self.provider = MockProvider()
        
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")
    
    @classmethod
    def get_instance(cls) -> "LLMClient":
        """Get or create singleton instance."""
        if cls._instance is None:
            provider = os.getenv("LLM_PROVIDER", "openai")
            cls._instance = cls(provider=provider)
        return cls._instance
    
    async def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate text."""
        return await self.provider.generate(prompt, temperature)
    
    async def generate_structured(
        self,
        prompt: str,
        schema: dict,
        temperature: float = 0.1
    ) -> dict:
        """Generate structured output."""
        return await self.provider.generate_structured(
            prompt, schema, temperature
        )
