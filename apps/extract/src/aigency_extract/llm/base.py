"""Base LLM provider interface."""

import os
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

from dotenv import load_dotenv

from aigency_extract.data.models import LLMProvider

# Load environment variables
load_dotenv()


class LLMInterface(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def complete(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Generate a completion for the given prompt."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this LLM provider is available (API key set, etc.)."""
        pass

    @property
    @abstractmethod
    def provider_name(self) -> LLMProvider:
        """Get the provider name."""
        pass

    @property
    @abstractmethod
    def available_models(self) -> List[str]:
        """Get a list of available models for this provider."""
        pass


class LLMFactory:
    """Factory for creating LLM provider instances."""

    _providers: Dict[LLMProvider, type] = {}

    @classmethod
    def register_provider(cls, provider_name: LLMProvider):
        """Register an LLM provider class."""
        def decorator(provider_class):
            cls._providers[provider_name] = provider_class
            return provider_class
        return decorator

    @classmethod
    def create(
        cls, 
        provider_name: Optional[str] = None, 
        model_name: Optional[str] = None
    ) -> LLMInterface:
        """Create an LLM provider instance."""
        # If no provider specified, use default from env or try to find any available
        if not provider_name:
            provider_name = os.getenv("DEFAULT_LLM_PROVIDER")
            
            # If still no provider, try to find any available
            if not provider_name:
                for provider in cls._providers.values():
                    instance = provider()
                    if instance.is_available():
                        return instance
                
                raise ValueError(
                    "No LLM provider specified and no available provider found. "
                    "Please set at least one API key in your .env file."
                )
        
        # Convert to enum
        try:
            provider_enum = LLMProvider(provider_name.lower())
        except ValueError:
            raise ValueError(f"Unknown LLM provider: {provider_name}")
        
        # Check if provider is registered
        if provider_enum not in cls._providers:
            raise ValueError(f"LLM provider {provider_name} is not registered")
        
        # Create instance
        provider_class = cls._providers[provider_enum]
        instance = provider_class()
        
        # Check if provider is available
        if not instance.is_available():
            raise ValueError(
                f"LLM provider {provider_name} is not available. "
                f"Please check your API key for this provider."
            )
        
        return instance


def get_llm(
    provider_name: Optional[str] = None, 
    model_name: Optional[str] = None
) -> LLMInterface:
    """Get an LLM provider instance."""
    return LLMFactory.create(provider_name, model_name)
