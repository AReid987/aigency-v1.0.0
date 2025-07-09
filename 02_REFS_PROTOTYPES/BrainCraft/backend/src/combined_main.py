from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Literal, Union
import base64
import io
import os
import re
import tempfile
import random
import urllib.parse
import requests
import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("braincraft-api")

# Initialize FastAPI app
app = FastAPI(
    title="BrainCraft API",
    description="Combined API for Text-to-Speech synthesis and chat",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request and response models
class TextRequest(BaseModel):
    text: str

class ChatRequest(BaseModel):
    message: str

class DiagramData(BaseModel):
    code: str
    type: str

class ChatResponse(BaseModel):
    response: str
    status: str
    diagram: Optional[DiagramData] = None

class AudioResponse(BaseModel):
    audio_base64: str

class ErrorResponse(BaseModel):
    status: str
    message: str

# Global settings
SETTINGS = {
    "USE_FREE_TTS": True,
    "TTS_LANGUAGE": "en",
    "LLM_PROVIDER": "gemini",  # Not actually used in simplified implementation
}

# Conversation state storage (in-memory for simplicity)
conversations = {}

class ConversationState:
    def __init__(self):
        self.messages = []
        self.current_diagram = None
        self.diagram_requirements = {}
        self.awaiting_feedback = False
        self.diagram_type = None
        self.last_activity = datetime.now()
        self.topics_mentioned = set()
        self.last_response_type = None
        self.has_offered_help = False
    
    def add_message(self, role: str, content: str):
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self.last_activity = datetime.now()
        
        # Track topics mentioned by user
        if role == "user":
            content_lower = content.lower()
            topics = ["app", "application", "system", "project", "software", "website", 
                     "platform", "service", "idea", "concept", "database", "workflow", 
                     "process", "architecture", "design"]
            for topic in topics:
                if topic in content_lower:
                    self.topics_mentioned.add(topic)

class DiagramRequirements:
    def __init__(self):
        self.purpose = None
        self.entities = []
        self.relationships = []
        self.flow_steps = []
        self.hierarchy = []
        self.data_points = []
        self.timeline_events = []
        self.diagram_type = None
        self.style_preferences = []
    
    def get_completeness_score(self):
        """Return a score from 0-1 indicating how complete the requirements are"""
        if not self.diagram_type:
            return 0.0
        
        score = 0.0
        
        if self.diagram_type == "flowchart":
            # For flowcharts, we need clear steps
            if self.flow_steps and len(self.flow_steps) >= 3:
                score = 0.9
            elif self.flow_steps and len(self.flow_steps) >= 2:
                score = 0.7
            elif self.flow_steps and len(self.flow_steps) >= 1:
                score = 0.4
            elif self.purpose and len(self.purpose) > 10:
                score = 0.2
            else:
                score = 0.1
        
        elif self.diagram_type in ["sequence", "class", "er"]:
            if self.entities and len(self.entities) >= 2:
                score = 0.7
                if self.relationships:
                    score = 0.9
            elif self.entities and len(self.entities) >= 1:
                score = 0.3
            elif self.purpose and len(self.purpose) > 10:
                score = 0.2
            else:
                score = 0.1
        
        elif self.diagram_type == "pie":
            if self.data_points and len(self.data_points) >= 2:
                score = 0.8
            elif self.purpose and len(self.purpose) > 10:
                score = 0.3
            else:
                score = 0.1
        
        elif self.diagram_type in ["gantt", "hierarchy"]:
            if (self.timeline_events and len(self.timeline_events) >= 2) or (self.hierarchy and len(self.hierarchy) >= 2):
                score = 0.8
            elif self.purpose and len(self.purpose) > 10:
                score = 0.3
            else:
                score = 0.1
        
        return min(score, 1.0)

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

class ConversationAgent:
    def __init__(self):
        self.diagram_types = {
            "flowchart": ["process", "workflow", "flow", "steps", "procedure"],
            "sequence": ["sequence", "interaction", "communication", "timeline", "chronological"],
            "class": ["class", "object", "structure", "relationship", "hierarchy"],
            "er": ["database", "entity", "data model", "schema"],
            "pie": ["pie", "distribution", "percentage", "proportion", "breakdown"],
            "gantt": ["gantt", "project", "schedule", "timeline", "planning"],
            "hierarchy": ["org chart", "hierarchy", "organization", "structure", "tree"]
        }
    
    def detect_diagram_intent(self, message: str) -> Optional[str]:
        """Detect if user wants to create a diagram and what type"""
        message_lower = message.lower()
        
        # Check for explicit diagram creation intent
        creation_keywords = ["create", "make", "draw", "design", "build", "generate", "show", "visualize"]
        diagram_keywords = ["diagram", "chart", "graph", "visualization", "flowchart", "model"]
        
        has_creation = any(keyword in message_lower for keyword in creation_keywords)
        has_diagram = any(keyword in message_lower for keyword in diagram_keywords)
        
        # Check for implicit diagram intent (app, system, project descriptions)
        implicit_keywords = ["app", "application", "system", "project", "software", "website", "platform", "service", "database", "architecture", "workflow", "process"]
        has_implicit = any(keyword in message_lower for keyword in implicit_keywords)
        
        if not (has_creation or has_diagram or has_implicit):
            return None
        
        # Detect diagram type
        for diagram_type, keywords in self.diagram_types.items():
            if any(keyword in message_lower for keyword in keywords):
                return diagram_type
        
        # For implicit intents, suggest general diagram creation
        if has_implicit:
            return "implicit"
        
        return "unknown"  # User wants a diagram but type unclear
    
    def extract_requirements(self, message: str, requirements: DiagramRequirements) -> DiagramRequirements:
        """Extract diagram requirements from user message"""
        message_lower = message.lower()
        
        # Extract entities/components
        if "entity" in message_lower or "table" in message_lower or "class" in message_lower:
            entities = re.findall(r'\b([A-Z][a-zA-Z]+)\b', message)
            requirements.entities.extend(entities)
        
        # Extract steps for flowcharts - improved logic
        step_indicators = ["first", "then", "next", "after", "finally", "step"]
        
        # Look for sequential patterns
        if any(indicator in message_lower for indicator in step_indicators):
            # Split by common separators and step indicators
            text = message.replace(',', '.')
            parts = re.split(r'[,.]|\bthen\b|\bnext\b|\bafter that\b|\bfinally\b', text, flags=re.IGNORECASE)
            
            for part in parts:
                part = part.strip()
                if len(part) > 5 and any(word in part.lower() for word in ['heat', 'grind', 'brew', 'add', 'mix', 'pour', 'start', 'end', 'check', 'wait']):
                    # Clean up the step
                    step = re.sub(r'^(first|then|next|after|finally|step \d+)[,\s]*', '', part, flags=re.IGNORECASE).strip()
                    if step and len(step) > 3:
                        requirements.flow_steps.append(step[:60])  # Limit length but keep readable
        
        # Also look for numbered steps
        numbered_steps = re.findall(r'\d+[.)]\s*([^.]+)', message)
        for step in numbered_steps:
            if len(step.strip()) > 3:
                requirements.flow_steps.append(step.strip()[:60])
        
        # Extract purpose
        purpose_indicators = ["for", "to", "about", "showing", "representing"]
        for indicator in purpose_indicators:
            if indicator in message_lower:
                # Extract text after purpose indicator
                parts = message_lower.split(indicator, 1)
                if len(parts) > 1:
                    requirements.purpose = parts[1].strip()[:100]  # Limit length
                break
        
        return requirements
    
    def generate_questions(self, requirements: DiagramRequirements) -> str:
        """Generate follow-up questions based on missing requirements"""
        if not requirements.diagram_type:
            return "I'd love to help you create a diagram! What kind of visualization are you looking for? For example, I can create flowcharts for processes, sequence diagrams for interactions, organizational charts, or database schemas."
        
        if requirements.diagram_type == "implicit":
            return "That sounds like an interesting project! I can help you visualize it with diagrams. Would you like me to create:\n• A system architecture diagram to show the overall structure?\n• A user flow diagram to show how people interact with it?\n• A database schema to model the data?\n• Or perhaps a different type of diagram?"
        
        completeness = requirements.get_completeness_score()
        
        if requirements.diagram_type == "flowchart":
            if not requirements.flow_steps or len(requirements.flow_steps) == 0:
                return "Great! I'll help you create a flowchart. Could you walk me through the main steps of the process? For example, what happens first, then what's next?"
            elif len(requirements.flow_steps) == 1:
                return f"Good start! I have: '{requirements.flow_steps[0]}'. What happens next in the process? Are there any decision points or alternative paths?"
            elif len(requirements.flow_steps) == 2:
                return f"Excellent! I have these steps: {', '.join(requirements.flow_steps)}. Are there any more steps, decision points, or branches in this process?"
            else:
                return "Perfect! I have enough information to create your flowchart."
        
        elif requirements.diagram_type == "sequence":
            if not requirements.entities or len(requirements.entities) == 0:
                return "Perfect! For a sequence diagram, I need to understand the interactions. What are the main participants or systems involved, and how do they communicate with each other?"
            elif len(requirements.entities) == 1:
                return f"Good! I have {requirements.entities[0]} as a participant. What other participants or systems are involved in this interaction?"
            else:
                return f"Great! I have these participants: {', '.join(requirements.entities)}. How do they interact with each other? What messages or calls do they exchange?"
        
        elif requirements.diagram_type == "class":
            if not requirements.entities or len(requirements.entities) == 0:
                return "Excellent! For a class diagram, could you describe the main entities or classes you want to model? What are their key attributes and relationships?"
            else:
                return f"Great! I have these classes: {', '.join(requirements.entities)}. What are the relationships between them? Any inheritance, composition, or associations?"
        
        elif requirements.diagram_type == "er":
            if not requirements.entities or len(requirements.entities) == 0:
                return "Great choice for data modeling! What are the main entities in your database? For example, if it's for an e-commerce system, you might have Customer, Order, Product, etc."
            else:
                return f"Perfect! I have these entities: {', '.join(requirements.entities)}. How are they related? What are the relationships and cardinalities between them?"
        
        return "Perfect! I have enough information to create your diagram."
    
    def generate_diagram_code(self, requirements: DiagramRequirements) -> str:
        """Generate mermaid diagram code based on requirements"""
        if requirements.diagram_type == "flowchart":
            return self._generate_flowchart(requirements)
        elif requirements.diagram_type == "sequence":
            return self._generate_sequence_diagram(requirements)
        elif requirements.diagram_type == "class":
            return self._generate_class_diagram(requirements)
        elif requirements.diagram_type == "er":
            return self._generate_er_diagram(requirements)
        else:
            # Default flowchart
            return self._generate_default_flowchart(requirements)
    
    def _generate_flowchart(self, requirements: DiagramRequirements) -> str:
        if requirements.flow_steps:
            code = "flowchart TD\n"
            prev_node = None
            for i, step in enumerate(requirements.flow_steps[:8]):  # Limit steps
                node_id = f"S{i+1}"
                clean_step = step.replace('"', "'")[:50]  # Clean and limit
                code += f'    {node_id}["{clean_step}"]\n'
                if prev_node:
                    code += f"    {prev_node} --> {node_id}\n"
                prev_node = node_id
            return code
        else:
            return self._generate_default_flowchart(requirements)
    
    def _generate_sequence_diagram(self, requirements: DiagramRequirements) -> str:
        code = "sequenceDiagram\n"
        entities = requirements.entities[:4] if requirements.entities else ["User", "System", "Database"]
        
        for entity in entities:
            code += f"    participant {entity[:10]}\n"
        
        # Add some basic interactions
        if len(entities) >= 2:
            code += f"    {entities[0]} ->> {entities[1]}: Request\n"
            code += f"    {entities[1]} -->> {entities[0]}: Response\n"
        
        return code
    
    def _generate_class_diagram(self, requirements: DiagramRequirements) -> str:
        code = "classDiagram\n"
        entities = requirements.entities[:5] if requirements.entities else ["User", "Order", "Product"]
        
        for entity in entities:
            code += f"    class {entity} {{\n"
            code += f"        +id: int\n"
            code += f"        +name: string\n"
            code += f"        +method()\n"
            code += f"    }}\n"
        
        # Add relationships
        if len(entities) >= 2:
            code += f"    {entities[0]} --> {entities[1]}\n"
        
        return code
    
    def _generate_er_diagram(self, requirements: DiagramRequirements) -> str:
        code = "erDiagram\n"
        entities = requirements.entities[:5] if requirements.entities else ["User", "Order", "Product"]
        
        for entity in entities:
            code += f"    {entity} {{\n"
            code += f"        int id\n"
            code += f"        string name\n"
            code += f"    }}\n"
        
        # Add relationships
        if len(entities) >= 2:
            code += f"    {entities[0]} ||--o{{ {entities[1]} : has\n"
        
        return code
    
    def _generate_default_flowchart(self, requirements: DiagramRequirements) -> str:
        purpose = requirements.purpose or "process"
        return f"""flowchart TD
    A[Start {purpose}] --> B{{Check conditions}}
    B -->|Yes| C[Process step 1]
    B -->|No| D[Alternative path]
    C --> E[Process step 2]
    D --> E
    E --> F[End]"""

agent = ConversationAgent()

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
        audio_base64 = await google_translate_tts(text_request.text, SETTINGS["TTS_LANGUAGE"])
        return AudioResponse(audio_base64=audio_base64)
    except Exception as e:
        logger.error(f"Error in synthesize endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Speech synthesis error: {str(e)}")

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Natural conversational chat endpoint with intelligent diagram generation"""
    logger.info(f"Received chat request: {request.message[:100]}...")
    
    try:
        # Use a simple session ID (in production, this would be more sophisticated)
        session_id = "default_session"
        
        # Get or create conversation state
        if session_id not in conversations:
            conversations[session_id] = ConversationState()
        
        conv_state = conversations[session_id]
        conv_state.add_message("user", request.message)
        
        user_message = request.message.strip()
        
        # Handle greeting
        if not conv_state.messages or len([m for m in conv_state.messages if m["role"] == "user"]) == 1:
            if any(greeting in user_message.lower() for greeting in ["hello", "hi", "hey", "greetings"]):
                response = "Hello! I'm your BrainCraft assistant. I specialize in creating diagrams and visualizations. What would you like to work on today? I can help you create flowcharts, sequence diagrams, class diagrams, database schemas, and more!"
                conv_state.add_message("assistant", response)
                conv_state.last_response_type = "greeting"
                return ChatResponse(response=response, status="success")
        
        # Handle feedback on existing diagram
        if conv_state.awaiting_feedback and conv_state.current_diagram:
            feedback_lower = user_message.lower()
            
            if any(positive in feedback_lower for positive in ["good", "great", "perfect", "yes", "looks good", "approve"]):
                response = "Excellent! I'm glad the diagram meets your needs. Is there anything else you'd like me to help you visualize, or would you like to make any refinements to this diagram?"
                conv_state.awaiting_feedback = False
                conv_state.add_message("assistant", response)
                return ChatResponse(response=response, status="success")
            
            elif any(negative in feedback_lower for negative in ["no", "not quite", "change", "modify", "different"]):
                response = "I understand you'd like some changes. Could you tell me specifically what you'd like me to adjust? For example, should I add more steps, change the relationships, or modify the structure?"
                conv_state.awaiting_feedback = False
                conv_state.add_message("assistant", response)
                return ChatResponse(response=response, status="success")
            
            else:
                # Treat as modification request
                if not conv_state.diagram_requirements:
                    conv_state.diagram_requirements = DiagramRequirements()
                    conv_state.diagram_requirements.diagram_type = conv_state.current_diagram.get("type", "flowchart")
                
                # Extract new requirements
                conv_state.diagram_requirements = agent.extract_requirements(user_message, conv_state.diagram_requirements)
                
                # Generate updated diagram
                new_diagram_code = agent.generate_diagram_code(conv_state.diagram_requirements)
                conv_state.current_diagram = {
                    "code": new_diagram_code,
                    "type": conv_state.diagram_requirements.diagram_type
                }
                
                response = "I've updated the diagram based on your feedback. How does this version look?"
                conv_state.awaiting_feedback = True
                conv_state.add_message("assistant", response)
                
                return ChatResponse(
                    response=response,
                    status="success",
                    diagram=DiagramData(
                        code=new_diagram_code,
                        type=conv_state.diagram_requirements.diagram_type
                    )
                )
        
        # Detect diagram creation intent
        diagram_intent = agent.detect_diagram_intent(user_message)
        
        if diagram_intent == "implicit":
            # Handle implicit diagram intent (user mentioned app/system but no specific diagram type)
            response = "That sounds like an interesting project! I can help you visualize different aspects of it with diagrams. For example, I can create:\n• System architecture diagrams to show overall structure\n• User flow diagrams for user interactions\n• Database schemas for data modeling\n• Process flowcharts for workflows\n• Class diagrams for software structure\n\nWhat aspect would you like to explore first?"
            conv_state.add_message("assistant", response)
            conv_state.last_response_type = "diagram_offer"
            conv_state.has_offered_help = True
            return ChatResponse(response=response, status="success")
        
        elif diagram_intent:
            # Initialize or update requirements
            if not conv_state.diagram_requirements:
                conv_state.diagram_requirements = DiagramRequirements()
            
            if diagram_intent != "unknown":
                conv_state.diagram_requirements.diagram_type = diagram_intent
            
            # Extract requirements from message
            conv_state.diagram_requirements = agent.extract_requirements(user_message, conv_state.diagram_requirements)
            
            # Check if we have enough information
            completeness = conv_state.diagram_requirements.get_completeness_score()
            
            if completeness >= 0.6:  # Sufficient information to create diagram
                diagram_code = agent.generate_diagram_code(conv_state.diagram_requirements)
                conv_state.current_diagram = {
                    "code": diagram_code,
                    "type": conv_state.diagram_requirements.diagram_type or "flowchart"
                }
                
                response = "Here's the diagram based on your requirements. How does this look? Feel free to ask for any modifications or improvements!"
                conv_state.awaiting_feedback = True
                conv_state.add_message("assistant", response)
                
                return ChatResponse(
                    response=response,
                    status="success",
                    diagram=DiagramData(
                        code=diagram_code,
                        type=conv_state.current_diagram["type"]
                    )
                )
            else:
                # Need more information
                question = agent.generate_questions(conv_state.diagram_requirements)
                conv_state.add_message("assistant", question)
                return ChatResponse(response=question, status="success")
        
        # Continue gathering requirements if already in diagram creation mode
        elif conv_state.diagram_requirements and not conv_state.awaiting_feedback:
            conv_state.diagram_requirements = agent.extract_requirements(user_message, conv_state.diagram_requirements)
            completeness = conv_state.diagram_requirements.get_completeness_score()
            
            if completeness >= 0.6:
                diagram_code = agent.generate_diagram_code(conv_state.diagram_requirements)
                conv_state.current_diagram = {
                    "code": diagram_code,
                    "type": conv_state.diagram_requirements.diagram_type or "flowchart"
                }
                
                response = "Perfect! Based on our conversation, I've created this diagram for you. What do you think?"
                conv_state.awaiting_feedback = True
                conv_state.add_message("assistant", response)
                
                return ChatResponse(
                    response=response,
                    status="success",
                    diagram=DiagramData(
                        code=diagram_code,
                        type=conv_state.current_diagram["type"]
                    )
                )
            else:
                question = agent.generate_questions(conv_state.diagram_requirements)
                conv_state.add_message("assistant", question)
                return ChatResponse(response=question, status="success")
        
        # Handle general conversation
        else:
            if "tts" in user_message.lower() or "speech" in user_message.lower() or "voice" in user_message.lower():
                response = "I can convert any of my messages to speech! Just click the speaker icon next to my responses to hear them read aloud. This feature uses a free text-to-speech service."
                conv_state.last_response_type = "tts_info"
            elif any(word in user_message.lower() for word in ["app", "application", "system", "project", "software", "website", "platform", "service", "idea", "concept"]):
                # Avoid repeating the same offer if we already made it
                if conv_state.last_response_type == "diagram_offer" or conv_state.has_offered_help:
                    # Build on what they mentioned instead of repeating the offer
                    mentioned_topics = [topic for topic in conv_state.topics_mentioned if topic in user_message.lower()]
                    if mentioned_topics:
                        response = f"Tell me more about your {mentioned_topics[0]}! What's the main functionality or purpose? Understanding the key features will help me suggest the most useful type of diagram to create."
                    else:
                        response = "Interesting! Can you tell me more about what this involves? For example, are there specific processes, user interactions, or data relationships you'd like to map out?"
                else:
                    response = "That sounds like an interesting project! I can help you visualize different aspects of it with diagrams. For example, I can create:\n• System architecture diagrams\n• User flow diagrams\n• Database schemas\n• Process flowcharts\n• Class diagrams\n\nWhat aspect would you like to explore first?"
                    conv_state.has_offered_help = True
                conv_state.last_response_type = "diagram_offer"
            elif conv_state.topics_mentioned and not conv_state.has_offered_help:
                # User has mentioned project-related topics before, be more specific
                topics_list = list(conv_state.topics_mentioned)
                response = f"I see you mentioned a {topics_list[0]} earlier. Would you like me to help visualize any part of it? I can create diagrams to show user flows, system architecture, data relationships, or process workflows."
                conv_state.has_offered_help = True
                conv_state.last_response_type = "specific_offer"
            else:
                # Avoid the generic response if we've already given it
                if conv_state.last_response_type == "generic_help":
                    response = "What would you like to work on? You can describe any process, system, or concept and I'll help you create a visual representation of it."
                else:
                    response = "I'm here to help you create diagrams and visualizations! You can ask me to create flowcharts, sequence diagrams, organizational charts, database schemas, and more. What would you like to visualize today?"
                conv_state.last_response_type = "generic_help"
            
            conv_state.add_message("assistant", response)
            return ChatResponse(response=response, status="success")
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return ChatResponse(
            response=f"I apologize, but I encountered an error. Could you please try rephrasing your request?",
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
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting BrainCraft API on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)