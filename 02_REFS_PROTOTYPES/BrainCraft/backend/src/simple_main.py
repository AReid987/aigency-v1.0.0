from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import base64
import requests
import urllib.parse
import random
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("braincraft-api")

# Initialize FastAPI app
app = FastAPI(
    title="BrainCraft API",
    description="Simple API for Text-to-Speech synthesis",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request and response models
class TextRequest(BaseModel):
    text: str

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    status: str
    diagram: Optional[dict] = None

class AudioResponse(BaseModel):
    audio_base64: str

class ErrorResponse(BaseModel):
    status: str
    message: str

# Simple Google Translate TTS service
async def google_translate_tts(text: str, lang: str = "en") -> str:
    """Synthesize speech using Google Translate's TTS (free, no API key required)"""
    logger.info("Using Google Translate for TTS")
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
        logger.info("Successfully synthesized speech")
        return audio_base64
        
    except Exception as e:
        logger.error(f"Error synthesizing speech: {str(e)}")
        raise Exception(f"Failed to synthesize speech: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "Welcome to BrainCraft API",
        "docs_url": "/docs",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    logger.debug("Health check requested")
    return {
        "status": "healthy",
        "service": "BrainCraft API",
        "version": "1.0.0"
    }

@app.post("/api/synthesize", response_model=AudioResponse)
async def synthesize_speech(text_request: TextRequest):
    """Synthesize speech using Google Translate TTS"""
    logger.info(f"Received synthesis request: {text_request.text[:100]}...")
    try:
        audio_base64 = await google_translate_tts(text_request.text)
        return AudioResponse(audio_base64=audio_base64)
    except Exception as e:
        logger.error(f"Error in synthesize endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Speech synthesis error: {str(e)}")

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Simple chat endpoint that returns an engaging response"""
    logger.info(f"Received chat request: {request.message[:100]}...")
    try:
        # Create a more engaging response based on the user's message
        user_message = request.message.lower()
        
        # Check for common question types
        if "hello" in user_message or "hi" in user_message:
            response = "👋 Hello! I'm your BrainCraft assistant. How can I help you today? Try asking me to create a diagram or explore my text-to-speech capabilities by clicking the speaker icon on my messages."
        
        elif "diagram" in user_message or "chart" in user_message or "graph" in user_message:
            # Example flowchart
            diagram_code = "flowchart TD\n    A[Start] --> B{Is it working?}\n    B -->|Yes| C[Great!]\n    B -->|No| D[Debug]\n    D --> B"
            response = "Here's a simple flowchart diagram! In the full version, I can create custom diagrams based on your requirements. Try out the text-to-speech feature by clicking the speaker icon next to my message."
            return ChatResponse(
                response=response,
                status="success",
                diagram={
                    "code": diagram_code,
                    "type": "flowchart"
                }
            )
            
        elif "speech" in user_message or "tts" in user_message or "speak" in user_message:
            response = "I can convert text to speech! Click the speaker icon next to any of my messages to hear them spoken aloud. This uses a free TTS service that works without requiring any API keys."
            
        else:
            response = f"Thanks for your message! The BrainCraft assistant is running in demo mode with simplified functionality. Try asking about diagrams or text-to-speech capabilities.\n\nYou can also click the speaker icon next to this message to hear it read aloud using our free TTS service."
            
        return ChatResponse(
            response=response,
            status="success"
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return ChatResponse(
            response=f"Error: {str(e)}",
            status="error"
        )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": str(exc)}
    )

if __name__ == "__main__":
    import uvicorn
    port = 8000
    logger.info(f"Starting BrainCraft API on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)