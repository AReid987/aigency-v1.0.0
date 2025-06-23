"""
Survey Agent - Core automation logic with enhanced browser viewing
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from enum import Enum
from datetime import datetime

from .stagehand_integration import EnhancedSurveyAgent

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent status enumeration"""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"
    RESTING = "resting"


class SurveyAgent:
    """Main survey automation agent with browser viewing capabilities"""
    
    def __init__(self):
        self.status = AgentStatus.IDLE
        self.current_task: Optional[str] = None
        self.current_live_view_url: Optional[str] = None
        self.stats = {
            "surveys_completed": 0,
            "total_runtime": 0,
            "errors": 0,
            "last_run": None,
            "sessions_with_viewing": 0
        }
        self._stop_event = asyncio.Event()
        self._pause_event = asyncio.Event()
        
        # Enhanced automation with viewing capabilities
        self.enhanced_agent = EnhancedSurveyAgent()
        
    async def start_survey_task(self, survey_config: Dict[str, Any]) -> bool:
        """Start a survey automation task with browser viewing"""
        try:
            logger.info(f"Starting survey task: {survey_config.get('name', 'Unknown')}")
            self.status = AgentStatus.RUNNING
            self.current_task = survey_config.get('name')
            
            # Default user profile (should come from config in production)
            user_profile = {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "age": 30,
                "location": "New York, NY",
                "ageRange": "25-35"
            }
            
            # Check if enhanced viewing is enabled
            if survey_config.get('enable_viewing', True):
                logger.info("Running survey with browser viewing enabled")
                result = await self.enhanced_agent.run_survey_with_viewing(
                    survey_config, user_profile
                )
                
                if result['success']:
                    self.current_live_view_url = result.get('live_view_url')
                    self.stats["sessions_with_viewing"] += 1
                    logger.info(f"Live view available: {self.current_live_view_url}")
                else:
                    logger.error(f"Enhanced automation failed: {result.get('error')}")
                    raise Exception(result.get('error', 'Unknown error'))
            else:
                # Fallback to traditional automation
                logger.info("Running survey with traditional automation")
                result = await self._run_traditional_survey(survey_config, user_profile)
            
            self.stats["surveys_completed"] += 1
            self.stats["last_run"] = datetime.now().isoformat()
            self.status = AgentStatus.IDLE
            self.current_task = None
            self.current_live_view_url = None
            
            logger.info("Survey task completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Survey task failed: {str(e)}")
            self.status = AgentStatus.ERROR
            self.stats["errors"] += 1
            self.current_live_view_url = None
            return False
    
    async def _run_traditional_survey(self, survey_config: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Run traditional survey automation using your existing scripts"""
        # This is where you'd integrate your combined_skyvern_script.py
        logger.info("Executing combined_skyvern_script.py logic")
        
        # Import and run your existing script logic
        # For now, simulate the work
        await asyncio.sleep(5)  # Simulate survey completion time
        
        return {
            "method": "traditional",
            "script": "combined_skyvern_script.py",
            "status": "completed"
        }
    
    def pause(self):
        """Pause the agent"""
        logger.info("Pausing agent")
        self.status = AgentStatus.PAUSED
        self._pause_event.set()
    
    def resume(self):
        """Resume the agent"""
        logger.info("Resuming agent")
        self.status = AgentStatus.RUNNING
        self._pause_event.clear()
    
    def stop(self):
        """Stop the agent"""
        logger.info("Stopping agent")
        self._stop_event.set()
        self.status = AgentStatus.IDLE
        self.current_live_view_url = None
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "status": self.status.value,
            "current_task": self.current_task,
            "live_view_url": self.current_live_view_url,
            "stats": self.stats
        }
    
    def get_live_view_url(self) -> Optional[str]:
        """Get the current live view URL"""
        return self.current_live_view_url
