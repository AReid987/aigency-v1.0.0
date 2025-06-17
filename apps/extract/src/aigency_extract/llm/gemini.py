"""Google Gemini provider implementation."""

import os
from typing import List, Optional

import httpx

from aigency_extract.data.models import LLMProvider
from aigency_extract.llm.base import LLMFactory, LLMInterface


@LLMFactory.register_provider(LLMProvider.GEMINI)
class GeminiProvider(LLMInterface):
    """Google Gemini provider implementation."""

    def __init__(self):
        """Initialize the Gemini provider."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.api_base = "https://generativelanguage.googleapis.com/v1beta"
        self.default_model = os.getenv("DEFAULT_LLM_MODEL", "gemini-1.5-pro")
        
        # Available models
        self._models = [
            "gemini-1.0-pro",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
        ]

    def complete(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Generate a completion using Google Gemini."""
        if not self.is_available():
            raise ValueError("Gemini API key not set")
        
        model = self.default_model
        
        # Prepare messages
        contents = []
        if system_prompt:
            contents.append({
                "role": "system",
                "parts": [{"text": system_prompt}]
            })
        
        contents.append({
            "role": "user",
            "parts": [{"text": prompt}]
        })
        
        data = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
                "topP": 0.95,
                "topK": 40,
            },
        }
        
        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(
                    f"{self.api_base}/models/{model}:generateContent?key={self.api_key}",
                    json=data,
                )
                response.raise_for_status()
                
                result = response.json()
                return result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            raise RuntimeError(f"Error calling Gemini API: {str(e)}")

    def is_available(self) -> bool:
        """Check if Gemini API is available."""
        return bool(self.api_key)

    @property
    def provider_name(self) -> LLMProvider:
        """Get the provider name."""
        return LLMProvider.GEMINI

    @property
    def available_models(self) -> List[str]:
        """Get a list of available models."""
        return self._models
