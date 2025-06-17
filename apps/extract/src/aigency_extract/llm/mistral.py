"""Mistral AI provider implementation."""

import os
from typing import List, Optional

import httpx

from aigency_extract.data.models import LLMProvider
from aigency_extract.llm.base import LLMFactory, LLMInterface


@LLMFactory.register_provider(LLMProvider.MISTRAL)
class MistralProvider(LLMInterface):
    """Mistral AI provider implementation."""

    def __init__(self):
        """Initialize the Mistral provider."""
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.api_base = "https://api.mistral.ai/v1"
        self.default_model = os.getenv("DEFAULT_LLM_MODEL", "mistral-large-latest")
        
        # Available models
        self._models = [
            "mistral-tiny",
            "mistral-small",
            "mistral-medium",
            "mistral-large-latest",
        ]

    def complete(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Generate a completion using Mistral AI."""
        if not self.is_available():
            raise ValueError("Mistral API key not set")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
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
            raise RuntimeError(f"Error calling Mistral API: {str(e)}")

    def is_available(self) -> bool:
        """Check if Mistral API is available."""
        return bool(self.api_key)

    @property
    def provider_name(self) -> LLMProvider:
        """Get the provider name."""
        return LLMProvider.MISTRAL

    @property
    def available_models(self) -> List[str]:
        """Get a list of available models."""
        return self._models
