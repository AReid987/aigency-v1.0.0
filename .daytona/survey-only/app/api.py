"""
API routes for the Survey Automation Framework
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

router = APIRouter()

# Global agent instance (will be injected from main.py)
agent = None

def set_agent(agent_instance):
    """Set the global agent instance"""
    global agent
    agent = agent_instance


class SurveyConfig(BaseModel):
    """Survey configuration model"""
    name: str
    url: str
    profile: str = "default"
    enable_viewing: bool = True
    use_ai: bool = False
    settings: Dict[str, Any] = {}


@router.get("/status")
async def get_status():
    """Get agent status"""
    if agent:
        return agent.get_status()
    return {
        "status": "not_initialized",
        "current_task": None,
        "live_view_url": None,
        "stats": {
            "surveys_completed": 0,
            "total_runtime": 0,
            "errors": 0,
            "sessions_with_viewing": 0
        }
    }


@router.get("/live-view")
async def get_live_view():
    """Get the current live view URL"""
    if agent:
        live_view_url = agent.get_live_view_url()
        if live_view_url:
            return {
                "available": True,
                "url": live_view_url,
                "status": "active"
            }
    
    return {
        "available": False,
        "url": None,
        "status": "inactive"
    }


@router.post("/agent/pause")
async def pause_agent():
    """Pause the agent"""
    if agent:
        agent.pause()
        return {"message": "Agent paused", "status": "paused"}
    raise HTTPException(status_code=503, detail="Agent not available")


@router.post("/agent/resume")
async def resume_agent():
    """Resume the agent"""
    if agent:
        agent.resume()
        return {"message": "Agent resumed", "status": "running"}
    raise HTTPException(status_code=503, detail="Agent not available")


@router.post("/survey/start")
async def start_survey(config: SurveyConfig):
    """Start a survey task"""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not available")
    
    survey_config = {
        "name": config.name,
        "url": config.url,
        "profile": config.profile,
        "enable_viewing": config.enable_viewing,
        "use_ai": config.use_ai,
        "settings": config.settings
    }
    
    # Start the survey task asynchronously
    success = await agent.start_survey_task(survey_config)
    
    if success:
        status = agent.get_status()
        return {
            "message": f"Survey '{config.name}' completed successfully",
            "success": True,
            "live_view_url": status.get("live_view_url"),
            "stats": status.get("stats")
        }
    else:
        raise HTTPException(status_code=500, detail="Survey task failed")


@router.get("/jobs")
async def get_scheduled_jobs():
    """Get scheduled jobs"""
    # TODO: Get actual scheduled jobs from scheduler
    return {"jobs": []}


@router.get("/logs")
async def get_logs():
    """Get recent logs"""
    # TODO: Implement log retrieval
    return {"logs": []}


@router.get("/browser-options")
async def get_browser_options():
    """Get available browser viewing options"""
    return {
        "options": [
            {
                "name": "Stagehand (BrowserBase)",
                "description": "AI-powered browser automation with built-in viewing",
                "features": ["Live View", "AI Automation", "Recording", "Anti-Detection"],
                "status": "recommended",
                "requires_api_key": True
            },
            {
                "name": "X11 Forwarding + VNC",
                "description": "Traditional remote desktop viewing",
                "features": ["Full Desktop", "Free", "Any Browser"],
                "status": "available",
                "requires_api_key": False
            },
            {
                "name": "OpenOperator",
                "description": "Open-source AI browser automation",
                "features": ["Open Source", "AI-Powered", "Recording"],
                "status": "experimental",
                "requires_api_key": False
            }
        ],
        "current": "Stagehand (BrowserBase)"
    }
