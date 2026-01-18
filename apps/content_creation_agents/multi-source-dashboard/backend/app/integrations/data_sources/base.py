from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio
import httpx
from app.core.config import settings

class BaseDataSource(ABC):
    """Abstract base class for all data source integrations"""
    
    def __init__(self, name: str, base_url: str, rate_limit: int = 60):
        self.name = name
        self.base_url = base_url
        self.rate_limit = rate_limit  # requests per minute
        self.last_request_time = 0
        self.request_count = 0
        
    async def _rate_limit_check(self):
        """Implement rate limiting"""
        current_time = datetime.now().timestamp()
        if current_time - self.last_request_time < 60:  # Within 1 minute
            if self.request_count >= self.rate_limit:
                wait_time = 60 - (current_time - self.last_request_time)
                await asyncio.sleep(wait_time)
                self.request_count = 0
                self.last_request_time = current_time
        else:
            self.request_count = 0
            self.last_request_time = current_time
        
        self.request_count += 1
    
    async def _make_request(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request with rate limiting"""
        await self._rate_limit_check()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
    
    @abstractmethod
    async def fetch_latest_content(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Fetch latest content from the data source"""
        pass
    
    @abstractmethod
    async def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate configuration for this data source"""
        pass
    
    @abstractmethod
    def get_config_schema(self) -> Dict[str, Any]:
        """Return JSON schema for configuration validation"""
        pass