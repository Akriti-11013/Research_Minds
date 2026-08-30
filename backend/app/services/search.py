"""
Search Service - Handles web search and source retrieval.

Supports multiple providers: Tavily, SerpAPI, DuckDuckGo
"""

from typing import Optional
from app.models.state import Source


class SearchProvider:
    """Base class for search providers."""
    
    async def search(self, query: str, max_results: int = 5) -> list[Source]:
        raise NotImplementedError


class TavilySearchProvider(SearchProvider):
    """Tavily API - AI-native search optimized for research."""
    
    def __init__(self, api_key: str):
        try:
            from tavily import AsyncTavilyClient
        except ImportError:
            try:
                from tavily import AsyncTavily
            except ImportError:
                raise ImportError(
                    "tavily not installed. Install with: pip install tavily-python"
                )
            self.client = AsyncTavily(api_key=api_key)
            return

        self.client = AsyncTavilyClient(api_key=api_key)
    
    async def search(self, query: str, max_results: int = 5) -> list[Source]:
        """Search using Tavily API."""
        try:
            response = await self.client.search(
                query=query,
                max_results=max_results,
                include_answer=True
            )
            
            sources: list[Source] = []
            if "results" in response:
                for result in response["results"][:max_results]:
                    sources.append({
                        "title": result.get("title", "Unknown"),
                        "url": result.get("url", ""),
                        "publisher": self._extract_domain(result.get("url", "")),
                        "snippet": result.get("content", "")[:500]  # Truncate to 500 chars
                    })
            
            return sources
        except Exception as e:
            print(f"Tavily search error: {e}")
            return []
    
    @staticmethod
    def _extract_domain(url: str) -> str:
        """Extract domain name from URL."""
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            # Remove 'www.' prefix if present
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        except:
            return "Unknown"


class MockSearchProvider(SearchProvider):
    """Mock search provider for testing."""
    
    async def search(self, query: str, max_results: int = 5) -> list[Source]:
        """Return mock search results."""
        return [
            {
                "title": f"Research Article: {query}",
                "url": "https://example.com/article",
                "publisher": "Example Publisher",
                "snippet": f"This is a mock research article about {query}. "
                           f"It provides insights into various aspects of the topic."
            },
            {
                "title": f"Analysis: Impact of {query}",
                "url": "https://research.example.com/analysis",
                "publisher": "Research Institute",
                "snippet": f"An in-depth analysis of {query} with data-driven insights "
                           f"and expert perspectives."
            }
        ][:max_results]


class SearchService:
    """Unified search service using different providers."""
    
    def __init__(self, provider: str = "mock", api_key: Optional[str] = None):
        self.provider_name = provider
        
        if provider == "tavily":
            if not api_key:
                raise ValueError("Tavily API key required")
            self.provider = TavilySearchProvider(api_key)
        
        elif provider == "mock":
            self.provider = MockSearchProvider()
        
        else:
            raise ValueError(f"Unknown search provider: {provider}")
    
    async def search(self, query: str, max_results: int = 5) -> list[Source]:
        """Search for sources."""
        return await self.provider.search(query, max_results)
    
    async def search_multiple_queries(
        self,
        queries: list[str],
        max_results_per_query: int = 3
    ) -> list[Source]:
        """Search multiple queries and deduplicate results."""
        all_sources: list[Source] = []
        seen_urls = set()
        
        for query in queries:
            results = await self.search(query, max_results_per_query)
            
            for source in results:
                url = source["url"]
                if url not in seen_urls:
                    all_sources.append(source)
                    seen_urls.add(url)
        
        return all_sources
