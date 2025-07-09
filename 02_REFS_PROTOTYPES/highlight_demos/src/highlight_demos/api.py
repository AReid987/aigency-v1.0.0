from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import os
import uvicorn

import ollama # Import the ollama library

# The DomainSpecificNLP class from nlp_system.py has been simplified
# as Ollama client now handles direct LLM interaction.
# We might not need to import or use it here anymore if all logic is in api.py.
# For now, let's comment out the import to ensure it's not accidentally used.
# try:
#     from .nlp_system import DomainSpecificNLP # Relative import
# except ImportError:
#     from nlp_system import DomainSpecificNLP # Absolute import

app = FastAPI(
    title="Knowledge Graph API",
    description="API for generating knowledge graphs from text using an NLP system.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for simplicity, adjust for production
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

# Configure logging for the API
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configure Ollama client
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL_NAME = os.environ.get("OLLAMA_MODEL_NAME", "gemma3:latest") # User specified local gemma3 model

ollama_client = None
# nlp_system_instance is removed as DomainSpecificNLP is no longer central to Ollama interaction.

@app.on_event("startup")
async def startup_event():
    global ollama_client
    logger.info(f"Attempting to connect to Ollama at {OLLAMA_HOST} with model {OLLAMA_MODEL_NAME}")
    try:
        ollama_client = ollama.Client(host=OLLAMA_HOST)
        # Check if the model is available by listing models
        # This also serves as a basic connection test.
        models_available = ollama_client.list()
        logger.info(f"Successfully connected to Ollama. Available models: {models_available.get('models')}")
        # Verify if the desired OLLAMA_MODEL_NAME is in the list
        model_found = any(model['name'] == OLLAMA_MODEL_NAME for model in models_available.get('models', []))
        if model_found:
            logger.info(f"Model {OLLAMA_MODEL_NAME} is available in Ollama.")
        else:
            logger.warning(f"Model {OLLAMA_MODEL_NAME} not found in Ollama. Please ensure it is pulled (e.g., 'ollama pull {OLLAMA_MODEL_NAME}').")
            # Depending on strictness, you might want to prevent startup or set a flag

    except Exception as e:
        logger.error(f"Failed to connect to Ollama: {e}", exc_info=True)
        ollama_client = None # Ensure client is None if connection failed
        # The application will start, but endpoints relying on Ollama will fail.

class TextIn(BaseModel):
    text: str

class GraphOut(BaseModel):
    nodes: list
    edges: list

class HealthStatus(BaseModel):
    status: str
    nlp_system: str

@app.post("/api/generate-graph", response_model=GraphOut)
async def generate_graph_endpoint(payload: TextIn):
    if ollama_client is None:
        logger.error("Ollama client is not available. Connection might have failed during startup.")
        raise HTTPException(status_code=500, detail="Ollama client not available. Check server logs.")

    try:
        input_text = payload.text
        logger.info(f"Received request to generate graph for text (first 50 chars): {input_text[:50]}...")

        # Define a prompt for knowledge graph extraction
        # This prompt needs to be designed to make the LLM output structured data (e.g., JSON)
        # that can be parsed into nodes and edges.
        prompt = f"""
Extract a knowledge graph from the following text. 
Identify entities as nodes and relationships between them as edges. 
Output the result as a JSON object with two keys: "nodes" and "edges".
Each node should be an object with an "id" (string) and "label" (string).
Each edge should be an object with a "source" (node id), "target" (node id), and "label" (string describing the relationship).

Text:
{input_text}

JSON Output:
"""

        logger.info(f"Sending prompt to Ollama model {OLLAMA_MODEL_NAME}...")
        response = ollama_client.chat(
            model=OLLAMA_MODEL_NAME,
            messages=[{'role': 'user', 'content': prompt}],
            format='json' # Request JSON output if the Ollama version and model support it
        )

        # The actual response structure from ollama.chat needs to be handled here.
        # It's usually response['message']['content']
        raw_json_output = response['message']['content']
        logger.debug(f"Raw JSON output from Ollama: {raw_json_output}")

        import json
        try:
            knowledge_graph_data = json.loads(raw_json_output)
            if not isinstance(knowledge_graph_data, dict) or \
               not all(k in knowledge_graph_data for k in ['nodes', 'edges']):
                logger.error(f"Ollama output is not in the expected JSON format: {raw_json_output}")
                raise HTTPException(status_code=500, detail="Failed to parse knowledge graph from LLM output: Unexpected format.")
        except json.JSONDecodeError as jde:
            logger.error(f"Failed to decode JSON from Ollama: {jde}. Output: {raw_json_output}")
            raise HTTPException(status_code=500, detail="Failed to parse knowledge graph from LLM output: Invalid JSON.")

        logger.info(f"Successfully generated graph with {len(knowledge_graph_data.get('nodes', []))} nodes and {len(knowledge_graph_data.get('edges', []))} edges.")
        return knowledge_graph_data

    except ollama.ResponseError as ore:
        logger.error(f"Ollama API error: {ore.error} (status code: {ore.status_code})", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Ollama API error: {ore.error}")
    except Exception as e:
        logger.error(f"Error processing /api/generate-graph: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health", response_model=HealthStatus)
async def health_check():
    ollama_status = "Unknown"
    if ollama_client:
        try:
            ollama_client.list() # Simple check to see if Ollama is responsive
            ollama_status = "Connected and Responsive"
        except Exception as e:
            logger.warning(f"Ollama client initialized but not responsive during health check: {e}")
            ollama_status = "Connected but Unresponsive"
    else:
        ollama_status = "Not Connected (or connection failed during startup)"
    
    return {"status": "healthy", "nlp_system": f"Ollama Status: {ollama_status}"}

if __name__ == '__main__':
    # This is for local development. For production, use a ASGI server like Uvicorn directly.
    logger.info("Starting FastAPI development server with Uvicorn...")
    uvicorn.run(app, host="0.0.0.0", port=5001, log_level="info")