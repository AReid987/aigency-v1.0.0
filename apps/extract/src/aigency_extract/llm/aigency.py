"""AIgency AI Gateway provider implementation."""

import os
from typing import List, Optional

import httpx

from aigency_extract.data.models import LLMProvider
from aigency_extract.llm.base import LLMFactory, LLMInterface


@LLMFactory.register_provider(LLMProvider.AIGENCY)
class AIgencyGatewayProvider(LLMInterface):
    """AIgency AI Gateway provider implementation."""

    def __init__(self):
        """Initialize the AIgency Gateway provider."""
        self.api_key = os.getenv("AIGENCY_AI_GATEWAY_KEY")
        self.api_base = os.getenv("AIGENCY_AI_GATEWAY_URL", "http://localhost:8000/v1")
        self.default_model = os.getenv("DEFAULT_LLM_MODEL", "default")
        
        # Available models will be fetched from the gateway
        self._models = ["default"]  # Will be populated when needed

    def complete(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Generate a completion using AIgency AI Gateway."""
        if not self.is_available():
            raise ValueError("AIgency AI Gateway not configured properly")
        
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        headers["Content-Type"] = "application/json"
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.default_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(
                    f"{self.api_base}/chat/completions",
                    headers=headers,
                    json=data,
                )
                response.raise_for_status()
                
                result = response.json()
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            raise RuntimeError(f"Error calling AIgency AI Gateway: {str(e)}")

    def is_available(self) -> bool:
        """Check if AIgency AI Gateway is available."""
        return bool(self.api_base)

    def fetch_available_models(self) -> List[str]:
        """Fetch available models from the gateway."""
        if not self.is_available():
            return ["default"]
        
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    f"{self.api_base}/models",
                    headers=headers,
                )
                response.raise_for_status()
                
                result = response.json()
                return [model["id"] for model in result["data"]]
        except Exception:
            return ["default"]

    @property
    def provider_name(self) -> LLMProvider:
        """Get the provider name."""
        return LLMProvider.AIGENCY

    @property
    def available_models(self) -> List[str]:
        """Get a list of available models."""
        if len(self._models) <= 1:
            try:
                self._models = self.fetch_available_models()
            except Exception:
                pass
        return self._models
