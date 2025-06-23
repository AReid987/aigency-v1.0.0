"""
Main entry point for the Survey Automation Framework
"""

import asyncio
import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .agent import SurveyAgent
from .api import router
from .scheduler import SurveyScheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Survey Automation Framework",
    description="Autonomous survey testing framework API",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

# Global instances
agent: SurveyAgent = None
scheduler: SurveyScheduler = None


@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    global agent, scheduler
    
    logger.info("Starting Survey Automation Framework...")
    
    # Initialize agent
    agent = SurveyAgent()
    
    # Inject agent into API routes
    from .api import set_agent
    set_agent(agent)
    
    # Initialize scheduler
    scheduler = SurveyScheduler(agent)
    scheduler.start()
    
    logger.info("Survey Automation Framework started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global scheduler
    
    logger.info("Shutting down Survey Automation Framework...")
    
    if scheduler:
        scheduler.stop()
    
    logger.info("Survey Automation Framework shut down")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Survey Automation Framework API",
        "status": "running",
        "version": "0.1.0"
    }


def main():
    """Run the application"""
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
