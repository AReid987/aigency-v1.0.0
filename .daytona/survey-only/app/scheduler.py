"""
Survey Scheduler - Manages automated survey execution
"""

import logging
from typing import Dict, Any
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from .agent import SurveyAgent

logger = logging.getLogger(__name__)


class SurveyScheduler:
    """Scheduler for automated survey tasks"""
    
    def __init__(self, agent: SurveyAgent):
        self.agent = agent
        self.scheduler = AsyncIOScheduler()
        self.is_running = False
        
    def start(self):
        """Start the scheduler"""
        if not self.is_running:
            logger.info("Starting survey scheduler")
            
            # Schedule survey tasks every 4 hours (as per requirements)
            self.scheduler.add_job(
                self._run_scheduled_survey,
                trigger=IntervalTrigger(hours=4),
                id="survey_task",
                name="Automated Survey Task"
            )
            
            self.scheduler.start()
            self.is_running = True
            logger.info("Survey scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        if self.is_running:
            logger.info("Stopping survey scheduler")
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("Survey scheduler stopped")
    
    async def _run_scheduled_survey(self):
        """Execute a scheduled survey task"""
        logger.info("Executing scheduled survey task")
        
        # Default survey configuration
        # TODO: Load from configuration file
        survey_config = {
            "name": "Scheduled Survey",
            "type": "automated",
            "timestamp": "now"
        }
        
        await self.agent.start_survey_task(survey_config)
    
    def add_custom_job(self, survey_config: Dict[str, Any], interval_hours: int = 4):
        """Add a custom survey job"""
        job_id = f"survey_{survey_config.get('name', 'custom')}"
        
        self.scheduler.add_job(
            lambda: self.agent.start_survey_task(survey_config),
            trigger=IntervalTrigger(hours=interval_hours),
            id=job_id,
            name=f"Survey: {survey_config.get('name', 'Custom')}"
        )
        
        logger.info(f"Added custom survey job: {job_id}")
    
    def get_jobs(self):
        """Get list of scheduled jobs"""
        return [
            {
                "id": job.id,
                "name": job.name,
                "next_run": job.next_run_time.isoformat() if job.next_run_time else None
            }
            for job in self.scheduler.get_jobs()
        ]
