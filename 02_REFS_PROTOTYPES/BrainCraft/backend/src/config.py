from pydantic_settings import BaseSettings
from typing import Optional, Literal, Union
from functools import lru_cache

class Settings(BaseSettings):
    # LLM Provider Configuration
    LLM_PROVIDER: Literal["mistral", "gemini", "openrouter"] = "mistral"
    
    # Mistral AI Configuration
    MISTRAL_API_KEY: Optional[str] = None
    MISTRAL_MODEL: str = "mistral-medium"
    
    # Google Gemini Configuration
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-1.5-pro"
    
    # OpenRouter Configuration
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_MODEL: str = "openai/gpt-4o"
    
    # Speech-to-Text (using OpenAI Whisper)
    OPENAI_API_KEY: Optional[str] = None
    
    # Text-to-Speech Configuration
    
    # Free TTS Options (no API key required)
    USE_FREE_TTS: bool = True  # Set to True to use free Google Translate TTS
    TTS_LANGUAGE: str = "en"   # Language code for Google Translate TTS (e.g. "en", "fr", "es", "de", "ja")
    
    # ElevenLabs TTS
    ELEVENLABS_API_KEY: Optional[str] = None
    ELEVENLABS_VOICE_ID: str = "EXAVITQu4vr4xnSDxMaL"  # Default: Rachel voice
    
    # OpenAI TTS
    OPENAI_TTS_MODEL: str = "tts-1"  # Options: "tts-1", "tts-1-hd"
    OPENAI_TTS_VOICE: str = "alloy"  # Options: "alloy", "echo", "fable", "onyx", "nova", "shimmer"
    
    # Azure Speech Service
    AZURE_SPEECH_KEY: Optional[str] = None
    AZURE_SPEECH_REGION: str = "eastus"
    AZURE_SPEECH_VOICE: str = "en-US-JennyNeural"
    
    # Google Cloud TTS
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None
    GOOGLE_TTS_VOICE: str = "en-US-Neural2-F"
    
    # Nari Labs Dia (Local TTS)
    DIA_ENABLE_LOCAL_TTS: bool = False  # Disabled by default, use cloud services instead
    DIA_SEED: Optional[int] = None  # Optional seed for voice consistency, None for random
    DIA_COMPUTE_DTYPE: str = "float32"  # Options: "float16", "bfloat16", "float32"
    DIA_USE_COMPILE: bool = False  # Enable PyTorch compilation for faster inference

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 