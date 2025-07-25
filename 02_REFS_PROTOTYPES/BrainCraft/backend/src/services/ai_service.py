from typing import Dict, Any, List, Optional, Union
import os
import re
import requests
from dotenv import load_dotenv
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from pydantic import BaseModel
from ..config import get_settings
from ..utils.logger import setup_logger

logger = setup_logger('ai_service')

load_dotenv(override=True)

class AIServiceError(Exception):
    """Custom exception for AI service errors"""
    pass

class DiagramResponse(BaseModel):
    """Response model for diagram generation"""
    diagram_code: Optional[str] = None
    diagram_type: Optional[str] = None
    explanation: Optional[str] = None

class DiagramAgent:
    def __init__(self):
        logger.info("Initializing DiagramAgent")
        settings = get_settings()
        self.provider = settings.LLM_PROVIDER
        
        try:
            # Initialize LLM based on selected provider
            if self.provider == "mistral":
                self.llm = self._setup_mistral_llm()
            elif self.provider == "gemini":
                self.llm = self._setup_gemini_llm()
            elif self.provider == "openrouter":
                self.llm = self._setup_openrouter_llm()
            else:
                logger.error(f"Unsupported LLM provider: {self.provider}")
                raise AIServiceError(f"Unsupported LLM provider: {self.provider}")
            
            logger.debug("Initializing conversation memory")
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )
            
            # Define tools
            logger.debug("Setting up agent tools")
            self.tools = [
                Tool(
                    name="generate_mermaid",
                    description="Generate a Mermaid.js diagram from a description",
                    func=self._generate_mermaid_diagram
                ),
                Tool(
                    name="refine_mermaid",
                    description="Refine an existing Mermaid.js diagram",
                    func=self._refine_mermaid_diagram
                )
            ]
            
    def _setup_mistral_llm(self):
        """Initialize Mistral AI LLM"""
        settings = get_settings()
        api_key = settings.MISTRAL_API_KEY
        model = settings.MISTRAL_MODEL
        
        if not api_key:
            logger.error("MISTRAL_API_KEY not found in environment variables")
            raise AIServiceError("MISTRAL_API_KEY not found in environment variables")
            
        logger.debug(f"Setting up Mistral LLM with model: {model}")
        return ChatMistralAI(
            api_key=api_key,
            model=model,
            temperature=0.7
        )
        
    def _setup_gemini_llm(self):
        """Initialize Google Gemini LLM"""
        settings = get_settings()
        api_key = settings.GEMINI_API_KEY
        model = settings.GEMINI_MODEL
        
        if not api_key:
            logger.error("GEMINI_API_KEY not found in environment variables")
            raise AIServiceError("GEMINI_API_KEY not found in environment variables")
            
        logger.debug(f"Setting up Google Gemini LLM with model: {model}")
        return ChatGoogleGenerativeAI(
            google_api_key=api_key,
            model=model,
            temperature=0.7
        )
        
    def _setup_openrouter_llm(self):
        """Initialize OpenRouter LLM"""
        settings = get_settings()
        api_key = settings.OPENROUTER_API_KEY
        model = settings.OPENROUTER_MODEL
        
        if not api_key:
            logger.error("OPENROUTER_API_KEY not found in environment variables")
            raise AIServiceError("OPENROUTER_API_KEY not found in environment variables")
            
        logger.debug(f"Setting up OpenRouter LLM with model: {model}")
        return ChatOpenAI(
            openai_api_key=api_key,
            model=model,
            temperature=0.7,
            openai_api_base="https://openrouter.ai/api/v1"
        )
        
        # Create the agent with tools
        logger.debug("Creating agent with prompt template")
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an expert diagram creation assistant. You can:
            1. Generate Mermaid.js diagrams from descriptions
            2. Refine existing diagrams based on feedback
            3. Explain diagram concepts and syntax
            
            Always use the appropriate tools when working with diagrams.
            When generating diagrams, follow these rules:
            1. Always wrap Mermaid code in triple backticks with 'mermaid' language identifier
            2. Provide a brief explanation of the diagram, make it conversational and friendly, max 100 words
            3. Specify the type of diagram (e.g., flowchart, sequence, class, etc.)
            4. For emoji support:
               - Use Unicode emojis directly in node labels
               - Always wrap labels containing emojis in double quotes
               - Do not use them as node labels, only as text inside nodes
            """),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        logger.info("Creating agent executor")
        self.agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True
        )
        logger.info("DiagramAgent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AI service: {str(e)}", exc_info=True)
            raise AIServiceError(f"Failed to initialize AI service with provider {self.provider}: {str(e)}")

    def _extract_mermaid_code(self, text: str) -> Optional[DiagramResponse]:
        """Extract Mermaid code and metadata from text"""
        logger.debug(f"Extracting Mermaid code from text: {text[:100]}...")
        
        # Look for Mermaid code block
        mermaid_match = re.search(r'\`\`\`mermaid\n([\s\S]*?)\n\`\`\`', text)
        if not mermaid_match:
            logger.debug("No Mermaid code block found in text")
            return None

        # Extract diagram code
        diagram_code = mermaid_match.group(1).strip()
        logger.debug(f"Extracted diagram code: {diagram_code[:100]}...")

        # Determine diagram type
        diagram_type = "flowchart"  # default
        if diagram_code.startswith("sequenceDiagram"):
            diagram_type = "sequence"
        elif diagram_code.startswith("classDiagram"):
            diagram_type = "class"
        elif diagram_code.startswith("erDiagram"):
            diagram_type = "er"
        elif diagram_code.startswith("gantt"):
            diagram_type = "gantt"
        elif diagram_code.startswith("pie"):
            diagram_type = "pie"
        
        logger.debug(f"Detected diagram type: {diagram_type}")
        
        # Extract explanation (text before or after the code block)
        explanation = text.replace(mermaid_match.group(0), "").strip()
        logger.debug(f"Extracted explanation: {explanation[:100]}...")
        
        return DiagramResponse(
            diagram_code=diagram_code,
            diagram_type=diagram_type,
            explanation=explanation
        )

    def _generate_mermaid_diagram(self, description: str) -> str:
        """Generate a Mermaid diagram based on description"""
        logger.info(f"Generating Mermaid diagram for description: {description[:100]}...")
        try:
            messages = [
                {
                    "role": "system",
                    "content": """Create a valid Mermaid.js diagram based on the description.
                    1. Start with a brief explanation of what the diagram shows
                    2. Then provide the diagram code wrapped in triple backticks with 'mermaid' language identifier
                    3. End with any additional notes or explanations"""
                },
                {
                    "role": "user",
                    "content": description
                }
            ]
            
            logger.debug(f"Sending request to {self.provider} LLM")
            response = self.llm.invoke(messages)
            logger.debug(f"Received response from LLM: {response.content[:100]}...")
            return response.content
        except Exception as e:
            logger.error(f"Failed to generate diagram: {str(e)}", exc_info=True)
            raise AIServiceError(f"Failed to generate diagram: {str(e)}")

    def _refine_mermaid_diagram(self, current_code: str, feedback: str) -> str:
        """Refine an existing Mermaid diagram based on feedback"""
        logger.info(f"Refining Mermaid diagram with feedback: {feedback[:100]}...")
        try:
            messages = [
                {
                    "role": "system",
                    "content": """Improve the Mermaid.js diagram based on the feedback.
                    1. Start with a brief explanation of the changes made
                    2. Then provide the modified diagram code wrapped in triple backticks with 'mermaid' language identifier
                    3. End with any additional notes about the changes"""
                },
                {
                    "role": "user",
                    "content": f"Current diagram:\n{current_code}\n\nFeedback: {feedback}"
                }
            ]
            
            logger.debug(f"Sending refinement request to {self.provider} LLM")
            response = self.llm.invoke(messages)
            logger.debug(f"Received refined diagram: {response.content[:100]}...")
            return response.content
        except Exception as e:
            logger.error(f"Failed to refine diagram: {str(e)}", exc_info=True)
            raise AIServiceError(f"Failed to refine diagram: {str(e)}")

    async def chat(self, message: str) -> Dict[str, Any]:
        """Handle chat interactions using LangChain agent"""
        logger.info(f"Processing chat message: {message[:100]}...")
        try:
            # Get response from agent
            logger.debug("Invoking agent executor")
            response = await self.agent_executor.ainvoke({"input": message})
            output_text = response["output"]
            logger.debug(f"Received response from agent: {output_text[:100]}...")

            # Extract diagram if present
            diagram_data = self._extract_mermaid_code(output_text)
            
            if diagram_data:
                logger.info("Diagram found in response")
                return {
                    "response": diagram_data.explanation,
                    "diagram": {
                        "code": diagram_data.diagram_code,
                        "type": diagram_data.diagram_type
                    },
                    "status": "success"
                }
            else:
                logger.info("No diagram found in response")
                return {
                    "response": output_text,
                    "status": "success"
                }

        except Exception as e:
            logger.error(f"Error in chat processing: {str(e)}", exc_info=True)
            error_message = str(e)
            if "API_KEY" in error_message:
                error_message = "API key configuration error. Please contact support."
            elif "rate limit" in error_message.lower():
                error_message = "Too many requests. Please try again in a moment."
            
            return {
                "response": f"Error: {error_message}",
                "status": "error"
            }
