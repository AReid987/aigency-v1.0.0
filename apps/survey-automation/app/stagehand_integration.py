"""
Stagehand Integration for Python Backend
Provides browser viewing and AI-powered automation capabilities
"""

import asyncio
import subprocess
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class StagehandManager:
    """Python wrapper for Stagehand browser automation with viewing capabilities"""
    
    def __init__(self):
        self.current_session: Optional[Dict[str, Any]] = None
        self.node_script_path = Path(__file__).parent.parent / "stagehand-integration.js"
        
    async def start_survey_session(self, survey_url: str, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Start a new survey session with Stagehand"""
        try:
            # Call Node.js Stagehand script
            cmd = [
                "node", 
                "-e", 
                f"""
                const {{ SurveyStagehandManager }} = require('{self.node_script_path}');
                
                async function run() {{
                    const manager = new SurveyStagehandManager();
                    const session = await manager.startSurveySession('{survey_url}', {json.dumps(user_profile)});
                    console.log(JSON.stringify(session));
                }}
                
                run().catch(console.error);
                """
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                session_data = json.loads(stdout.decode())
                self.current_session = session_data
                logger.info(f"Stagehand session started: {session_data.get('liveViewUrl')}")
                return session_data
            else:
                error_msg = stderr.decode()
                logger.error(f"Failed to start Stagehand session: {error_msg}")
                raise Exception(f"Stagehand session failed: {error_msg}")
                
        except Exception as e:
            logger.error(f"Error starting Stagehand session: {str(e)}")
            raise
    
    async def fill_survey_with_ai(self, instructions: str) -> Dict[str, Any]:
        """Use AI to fill survey automatically"""
        if not self.current_session:
            raise Exception("No active Stagehand session")
        
        # Implementation would call Node.js script to execute AI filling
        # For now, return a mock response
        return {
            "success": True,
            "method": "ai_powered",
            "instructions": instructions
        }
    
    async def fill_survey_manually(self, field_mappings: Dict[str, str]) -> Dict[str, Any]:
        """Fill survey fields manually with precise control"""
        if not self.current_session:
            raise Exception("No active Stagehand session")
        
        # Implementation would call Node.js script for manual filling
        # For now, return a mock response
        return {
            "success": True,
            "method": "manual",
            "fields_filled": len(field_mappings)
        }
    
    async def take_screenshot(self) -> bytes:
        """Take a screenshot of the current browser state"""
        if not self.current_session:
            raise Exception("No active Stagehand session")
        
        # Implementation would call Node.js script to take screenshot
        # For now, return empty bytes
        return b""
    
    def get_live_view_url(self) -> Optional[str]:
        """Get the live view URL for the current session"""
        return self.current_session.get('liveViewUrl') if self.current_session else None
    
    def get_session_status(self) -> Dict[str, Any]:
        """Get current session status"""
        if self.current_session:
            return {
                "status": "active",
                "url": self.current_session.get('url'),
                "live_view_url": self.current_session.get('liveViewUrl'),
                "start_time": self.current_session.get('startTime')
            }
        return {"status": "inactive"}
    
    async def end_session(self) -> Dict[str, Any]:
        """End the current session and get recording"""
        if not self.current_session:
            return {"status": "no_active_session"}
        
        # Implementation would call Node.js script to end session
        session_summary = {
            "status": "completed",
            "session_data": self.current_session,
            "recording_url": "https://example.com/recording"  # Mock URL
        }
        
        self.current_session = None
        logger.info("Stagehand session ended")
        return session_summary


# Integration with existing agent
class EnhancedSurveyAgent:
    """Enhanced survey agent with Stagehand integration"""
    
    def __init__(self):
        self.stagehand = StagehandManager()
        self.traditional_automation = None  # Your existing automation logic
        
    async def run_survey_with_viewing(self, survey_config: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Run survey with browser viewing capabilities"""
        try:
            # Start Stagehand session for viewing
            session = await self.stagehand.start_survey_session(
                survey_config['url'], 
                user_profile
            )
            
            # Get live view URL for dashboard
            live_view_url = self.stagehand.get_live_view_url()
            
            # Choose automation method based on configuration
            if survey_config.get('use_ai', False):
                # Use AI-powered automation
                result = await self.stagehand.fill_survey_with_ai(
                    f"Complete this survey as {user_profile['name']}, "
                    f"age {user_profile['age']}, from {user_profile['location']}"
                )
            else:
                # Use your existing combined_skyvern_script.py logic
                result = await self._run_traditional_automation(survey_config, user_profile)
            
            # Take screenshot for verification
            screenshot = await self.stagehand.take_screenshot()
            
            # End session and get recording
            session_summary = await self.stagehand.end_session()
            
            return {
                "success": True,
                "live_view_url": live_view_url,
                "automation_result": result,
                "session_summary": session_summary,
                "screenshot_available": len(screenshot) > 0
            }
            
        except Exception as e:
            logger.error(f"Enhanced survey automation failed: {str(e)}")
            await self.stagehand.end_session()
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _run_traditional_automation(self, survey_config: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Run your existing automation scripts"""
        # This is where you'd integrate your combined_skyvern_script.py
        # For now, return a mock result
        return {
            "method": "traditional",
            "script": "combined_skyvern_script.py",
            "status": "completed"
        }
