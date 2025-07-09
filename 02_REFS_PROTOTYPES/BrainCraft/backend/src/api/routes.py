from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..services import DiagramAgent, AudioService
from ..services.ai_service import AIServiceError
from ..services.audio_service import AudioServiceError
from ..utils.logger import setup_logger
from ..config import get_settings
from ..utils.logger import setup_logger

logger = setup_logger('api_routes')

# Get TTS provider name from settings
settings = get_settings()
tts_provider = "free Google Translate TTS" if getattr(settings, "USE_FREE_TTS", False) else "configured TTS service"
logger.info(f"Using {tts_provider} for speech synthesis")

# Create router without prefix
router = APIRouter()
diagram_agent = DiagramAgent()
audio_service = AudioService()

class ChatRequest(BaseModel):
    message: str

class DiagramData(BaseModel):
    code: str
    type: str

class ChatResponse(BaseModel):
    response: str
    status: str
    diagram: Optional[DiagramData] = None

class AudioRequest(BaseModel):
    audio_base64: str

class TextRequest(BaseModel):
    text: str

class AudioResponse(BaseModel):
    audio_base64: str

class TranscriptionResponse(BaseModel):
    text: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle chat messages and generate responses"""
    logger.info(f"Received chat request: {request.message[:100]}...")
    try:
        logger.debug("Processing chat request with DiagramAgent")
        result = await diagram_agent.chat(message=request.message)
        logger.info("Successfully processed chat request")
        return result
    except AIServiceError as e:
        logger.error(f"AI service error in chat request: {str(e)}", exc_info=True)
        error_message = str(e)
        
        settings = get_settings()
        provider = settings.LLM_PROVIDER
        
        if "API_KEY" in error_message:
            error_detail = f"Missing or invalid {provider.upper()}_API_KEY. Please check your configuration."
        elif "rate limit" in error_message.lower():
            error_detail = f"{provider.capitalize()} API rate limit exceeded. Please try again later."
        else:
            error_detail = f"Error with {provider.capitalize()} AI service: {error_message}"
            
        raise HTTPException(status_code=500, detail=error_detail)
    except Exception as e:
        logger.error(f"Unexpected error processing chat request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.debug("Health check requested")
    return {
        "status": "healthy",
        "service": "BrainCraft API",
        "version": "1.0.0"
    }

@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(audio_request: AudioRequest):
    """Transcribe audio using OpenAI Whisper"""
    logger.info("Received transcription request")
    try:
        text = await audio_service.transcribe_audio(audio_request.audio_base64)
        return TranscriptionResponse(text=text)
    except AudioServiceError as e:
        logger.error(f"Audio service error in transcribe endpoint: {str(e)}", exc_info=True)
        error_message = str(e)
        
        if "OPENAI_API_KEY" in error_message:
            error_detail = "Missing or invalid OpenAI API key for transcription"
        else:
            error_detail = f"Transcription error: {error_message}"
            
        raise HTTPException(status_code=500, detail=error_detail)
    except Exception as e:
        logger.error(f"Unexpected error in transcribe endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected transcription error: {str(e)}")

@router.post("/synthesize", response_model=AudioResponse)
async def synthesize_speech(text_request: TextRequest):
    """Synthesize speech using configured TTS provider"""
    logger.info(f"Received synthesis request: {text_request.text[:100]}...")
    try:
        audio_base64 = await audio_service.synthesize_speech(text_request.text)
        return AudioResponse(audio_base64=audio_base64)
    except AudioServiceError as e:
        logger.error(f"Audio service error in synthesize endpoint: {str(e)}", exc_info=True)
        error_message = str(e)
        
        # Determine the error type based on the error message
        if "Dia" in error_message:
            error_detail = "Error with Dia TTS service. Is Dia running locally?"
        elif "Google Translate" in error_message:
            error_detail = "Error with Google Translate TTS. Check network connection or try with fewer characters."
        elif "ElevenLabs" in error_message:
            if "401" in error_message or "403" in error_message:
                error_detail = "Invalid ElevenLabs API key. Check your configuration."
            elif "429" in error_message:
                error_detail = "ElevenLabs rate limit exceeded. You may have used up your free tier quota."
            else:
                error_detail = f"ElevenLabs TTS error: {error_message}"
        elif "OpenAI" in error_message:
            if "API key" in error_message:
                error_detail = "Missing or invalid OpenAI API key for speech synthesis."
            else:
                error_detail = f"OpenAI TTS error: {error_message}"
        else:
            error_detail = f"Speech synthesis error: {error_message}"
            
        raise HTTPException(status_code=500, detail=error_detail)
    except Exception as e:
        logger.error(f"Unexpected error in synthesize endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected speech synthesis error: {str(e)}")
