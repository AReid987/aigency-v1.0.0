from typing import Dict, Any, Optional, Literal
import base64
import io
import os
import tempfile
import requests
import urllib.parse
import random
from openai import OpenAI
from ..config import get_settings
from ..utils.logger import setup_logger

# Import Dia only if available
try:
    from dia.model import Dia
    DIA_AVAILABLE = True
except ImportError:
    DIA_AVAILABLE = False
    logger = setup_logger('audio_service')
    logger.warning("Dia TTS not installed. Will attempt to use it if needed, but may fall back to free TTS options.")

logger = setup_logger('audio_service')

class AudioServiceError(Exception):
    """Custom exception for audio service errors"""
    pass

class AudioService:
    def __init__(self):
        logger.info("Initializing AudioService")
        settings = get_settings()
        self.settings = settings
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
        self.dia_settings = {
            "seed": settings.DIA_SEED,
            "compute_dtype": settings.DIA_COMPUTE_DTYPE,
            "use_compile": settings.DIA_USE_COMPILE
        }

        # Determine TTS provider
        self.tts_provider = self._determine_tts_provider()
        logger.info(f"Using TTS provider: {self.tts_provider}")

        # Initialize Dia only if needed and available
        self.dia_model = None
        if settings.DIA_ENABLE_LOCAL_TTS and DIA_AVAILABLE and self.tts_provider == "dia":
            try:
                logger.info(f"Loading Nari Labs Dia model with dtype: {self.dia_settings['compute_dtype']}")
                self.dia_model = Dia.from_pretrained(
                    "nari-labs/Dia-1.6B",
                    compute_dtype=self.dia_settings['compute_dtype']
                )
                logger.info("Successfully loaded Dia TTS model")
            except Exception as e:
                logger.error(f"Failed to load Dia TTS model: {str(e)}")
                logger.info("Will use Google Translate TTS as fallback")
                self.tts_provider = "gtranslate"
        elif settings.DIA_ENABLE_LOCAL_TTS and self.tts_provider == "dia":
            logger.warning("Dia is enabled but not installed. Will use Google Translate TTS instead.")
            self.tts_provider = "gtranslate"

    def _determine_tts_provider(self) -> Literal["gtranslate", "dia"]:
        """Determine which TTS provider to use based on available configuration"""
        settings = self.settings

        if hasattr(settings, "USE_FREE_TTS") and settings.USE_FREE_TTS:
            return "gtranslate"
        elif settings.DIA_ENABLE_LOCAL_TTS:
            return "dia"
        else:
            logger.info("No specific TTS provider configured. Using free Google Translate TTS.")
            return "gtranslate"

    async def transcribe_audio(self, audio_base64: str) -> str:
        """Transcribe audio using OpenAI Whisper"""
        logger.info("Processing transcription request")

        if not self.client:
            logger.error("OpenAI client not initialized. OPENAI_API_KEY may be missing.")
            raise AudioServiceError("OpenAI API key is required for transcription")

        try:
            # Decode base64 audio
            audio_bytes = base64.b64decode(audio_base64)

            # Create in-memory file object
            audio_file = io.BytesIO(audio_bytes)
            audio_file.name = "audio.wav"

            # Transcribe using OpenAI
            logger.debug("Sending request to OpenAI Whisper")
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

            logger.info("Successfully transcribed audio")
            return transcription.text

        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}", exc_info=True)
            raise AudioServiceError(f"Failed to transcribe audio: {str(e)}")

    async def _synthesize_with_google_translate(self, text: str) -> str:
        """Synthesize speech using Google Translate's TTS (free, no API key required)"""
        logger.info("Using Google Translate for TTS (free)")
        try:
            # Split text into smaller chunks (Google Translate has length limits)
            MAX_CHARS = 200
            text_chunks = []

            # Split by sentence if possible
            sentences = text.replace(".", ". ").replace("!", "! ").replace("?", "? ").split()
            current_chunk = ""

            for sentence in sentences:
                if len(current_chunk) + len(sentence) < MAX_CHARS:
                    current_chunk += " " + sentence if current_chunk else sentence
                else:
                    if current_chunk:
                        text_chunks.append(current_chunk)
                    current_chunk = sentence

            if current_chunk:
                text_chunks.append(current_chunk)

            # If somehow we have no chunks, just use the original text
            if not text_chunks:
                text_chunks = [text[:MAX_CHARS]]

            # Generate audio for each chunk
            all_audio_data = bytearray()

            for chunk in text_chunks:
                # Prepare the URL
                lang = getattr(self.settings, "TTS_LANGUAGE", "en")

                # Add some randomness to prevent caching/blocking
                query_id = random.randint(10000, 99999)

                # Build the URL for Google Translate TTS
                url = f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q={urllib.parse.quote(chunk)}&tl={lang}&ttsspeed=1&idx=0&textlen={len(chunk)}&tk={query_id}"

                # Make the request with a browser-like user agent
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Referer": "https://translate.google.com/",
                    "Accept-Language": "en-US,en;q=0.9"
                }

                response = requests.get(url, headers=headers)
                response.raise_for_status()

                # Append this chunk's audio to our complete audio
                all_audio_data.extend(response.content)

            # Convert audio bytes to base64
            audio_base64 = base64.b64encode(all_audio_data).decode('utf-8')
            logger.info("Successfully synthesized speech with Google Translate TTS")
            return audio_base64

        except Exception as e:
            logger.error(f"Error synthesizing speech with Google Translate: {str(e)}", exc_info=True)
            raise AudioServiceError(f"Failed to synthesize speech with Google Translate: {str(e)}")

    async def _synthesize_with_dia(self, text: str) -> str:
        """Synthesize speech using Nari Labs Dia"""
        logger.info("Using Dia for TTS")
        try:
            # Check if Dia is initialized
            if self.dia_model is None:
                logger.error("Dia TTS model not initialized")
                raise AudioServiceError("Dia TTS model not initialized. Check your configuration.")

            # Format text with speaker tags for Dia if not already formatted
            if not text.startswith("[S1]") and not text.startswith("[S2]"):
                logger.debug("Adding speaker tags to text")
                formatted_text = f"[S1] {text}"
            else:
                formatted_text = text
            
            logger.debug(f"Generating speech with Dia model using text: {formatted_text[:100]}...")
            
            # Set seed if provided
            generation_kwargs = {}
            if self.dia_settings['seed'] is not None:
                generation_kwargs['seed'] = self.dia_settings['seed']
            
            # Generate audio with Dia
            output = self.dia_model.generate(
                formatted_text, 
                use_torch_compile=self.dia_settings['use_compile'],
                verbose=True,
                **generation_kwargs
            )
            
            # Save audio to temporary file and read it back
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                try:
                    # Save audio to temp file
                    self.dia_model.save_audio(temp_file.name, output)
                    
                    # Read the file back
                    with open(temp_file.name, "rb") as f:
                        audio_data = f.read()
                finally:
                    # Clean up the temp file
                    os.unlink(temp_file.name)
            
            # Convert audio bytes to base64
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            logger.info("Successfully synthesized speech with Dia")
            return audio_base64
        
        except Exception as e:
            logger.error(f"Error synthesizing speech with Dia: {str(e)}", exc_info=True)
            raise AudioServiceError(f"Failed to synthesize speech with Dia: {str(e)}")

    async def synthesize_speech(self, text: str) -> str:
        """Synthesize speech using the configured TTS provider"""
        logger.info(f"Processing synthesis request: {text[:100]}...")
        
        try:
            # Route to the appropriate TTS provider
            if self.tts_provider == "gtranslate":
                return await self._synthesize_with_google_translate(text)
            elif self.tts_provider == "dia":
                try:
                    return await self._synthesize_with_dia(text)
                except Exception as e:
                    logger.error(f"Error with Dia TTS, falling back to Google Translate: {str(e)}")
                    return await self._synthesize_with_google_translate(text)
            else:
                # Fallback to Google Translate TTS as it's free
                logger.warning(f"Unknown TTS provider: {self.tts_provider}. Falling back to Google Translate TTS.")
                return await self._synthesize_with_google_translate(text)
        
        except Exception as e:
            logger.error(f"Error synthesizing speech: {str(e)}", exc_info=True)
            raise AudioServiceError(f"Failed to synthesize speech: {str(e)}")