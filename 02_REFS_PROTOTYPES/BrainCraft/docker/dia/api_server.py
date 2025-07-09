import os
import io
import base64
import tempfile
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
import logging
import torch

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("dia-api")

# Import Dia
try:
    from dia.model import Dia
    logger.info("Successfully imported Dia")
except ImportError as e:
    logger.error(f"Failed to import Dia: {str(e)}")
    raise

# Initialize FastAPI app
app = FastAPI(
    title="Dia TTS API",
    description="API for Nari Labs Dia Text-to-Speech model",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request and response models
class TTSRequest(BaseModel):
    text: str
    seed: Optional[int] = None
    compute_dtype: str = "float32"  # Use float32 for better CPU compatibility
    use_compile: bool = False  # Disable compilation by default for CPU compatibility
    audio_prompt: Optional[str] = None  # Base64 encoded audio for voice cloning

class TTSResponse(BaseModel):
    audio: str  # Base64 encoded audio

class HealthResponse(BaseModel):
    status: str
    version: str
    cuda_available: bool
    device: str

# Global model instance
model = None

def get_model(compute_dtype: str = "float32"):
    """Get or initialize the Dia model"""
    global model
    
    if model is None:
        # Check if CUDA is available and adjust compute_dtype if needed
        if not torch.cuda.is_available() and compute_dtype == "float16":
            logger.warning("CUDA not available, switching to float32 for better CPU compatibility")
            compute_dtype = "float32"
        
        logger.info(f"Loading Dia model with compute_dtype={compute_dtype} on {'CUDA' if torch.cuda.is_available() else 'CPU'}")
        try:
            model = Dia.from_pretrained("nari-labs/Dia-1.6B", compute_dtype=compute_dtype)
            logger.info("Successfully loaded Dia model")
        except Exception as e:
            logger.error(f"Failed to load Dia model: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to load Dia model: {str(e)}")
    
    return model

@app.post("/api/tts", response_model=TTSResponse)
async def tts(request: TTSRequest):
    """Generate speech from text using Dia"""
    logger.info(f"TTS request received: {request.text[:100]}...")
    
    try:
        # If CUDA is not available and use_compile is True, warn and disable it
        if not torch.cuda.is_available() and request.use_compile:
            logger.warning("CUDA not available, disabling torch.compile for CPU compatibility")
            request.use_compile = False
            
        # Get or initialize model with appropriate dtype for the hardware
        compute_dtype = request.compute_dtype
        if not torch.cuda.is_available() and compute_dtype == "float16":
            logger.warning("CUDA not available, switching to float32 for better CPU compatibility")
            compute_dtype = "float32"
            
        dia = get_model(compute_dtype=compute_dtype)
        
        # Format text with speaker tags if not already formatted
        if not request.text.startswith("[S1]") and not request.text.startswith("[S2]"):
            formatted_text = f"[S1] {request.text}"
        else:
            formatted_text = request.text
        
        # Set up generation kwargs
        generation_kwargs = {}
        if request.seed is not None:
            generation_kwargs['seed'] = request.seed
            
        # Generate audio
        logger.info(f"Generating audio on {'CUDA' if torch.cuda.is_available() else 'CPU'}...")
        output = dia.generate(
            formatted_text,
            use_torch_compile=request.use_compile,
            verbose=True,
            **generation_kwargs
        )
        
        # Save audio to temporary file and read it back
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            try:
                # Save audio to temp file
                dia.save_audio(temp_file.name, output)
                
                # Read the file back
                with open(temp_file.name, "rb") as f:
                    audio_data = f.read()
            finally:
                # Clean up the temp file
                os.unlink(temp_file.name)
        
        # Convert audio to base64
        audio_base64 = base64.b64encode(audio_data).decode("utf-8")
        
        logger.info("Successfully generated audio")
        return TTSResponse(audio=audio_base64)
    
    except Exception as e:
        logger.error(f"Error generating speech: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        cuda_available=torch.cuda.is_available(),
        device="cuda" if torch.cuda.is_available() else "cpu"
    )

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Dia TTS API is running",
        "documentation": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.environ.get("PORT", 5002))
    
    # Log hardware information
    logger.info(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        logger.info(f"CUDA device: {torch.cuda.get_device_name(0)}")
    else:
        logger.info("Running in CPU-only mode - speech generation will be slower")
    
    # Initialize model on startup to avoid cold start
    try:
        logger.info("Preloading Dia model...")
        # Use float32 by default on CPU for better compatibility
        default_dtype = "float32" if not torch.cuda.is_available() else "float16"
        get_model(compute_dtype=default_dtype)
    except Exception as e:
        logger.error(f"Failed to preload model: {str(e)}")
        logger.warning("The API server will start but model initialization failed. Will try again on first request.")
    
    # Run server
    logger.info(f"Starting Dia TTS API server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)