from typing import Literal
import openrouter
import groq
import anthropic

ModelProvider = Literal["openrouter", "groq", "anthropic", "ollama"]

class AIModelGateway:
    def __init__(self, provider: ModelProvider = "openrouter"):
        self.provider = provider
        self.clients = {
            "openrouter": openrouter.Client,
            "groq": groq.Client,
            "anthropic": anthropic.Client,
            "ollama": lambda: NotImplementedError("Ollama not implemented")
        }
        
    def analyze(self, content: str, model: str = None, **kwargs):
        """Unified analysis interface"""
        if self.provider == "openrouter":
            return self._analyze_openrouter(content, model, **kwargs)
        elif self.provider == "groq":
            return self._analyze_groq(content, model, **kwargs)
        # ... other providers
        
    def _analyze_openrouter(self, content: str, model: str = "gemini-pro", **kwargs):
        return openrouter.complete(
            model=model,
            prompt=f"Analyze this content: {content}",
            **kwargs
        )
        
    def _analyze_groq(self, content: str, model: str = "mixtral-8x7b", **kwargs):
        return groq.complete(
            model=model,
            prompt=f"Analyze: {content}",
            **kwargs
        )
        
    def switch_provider(self, new_provider: ModelProvider):
        self.provider = new_provider