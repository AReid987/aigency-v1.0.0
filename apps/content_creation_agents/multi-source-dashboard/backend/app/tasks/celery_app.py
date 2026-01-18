from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

# Create Celery instance
celery_app = Celery(
    "dashboard_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_CACHE_URL,
    include=[
        "app.tasks.data_collection",
        "app.tasks.content_processing",
        "app.tasks.publishing"
    ]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Periodic task schedule
celery_app.conf.beat_schedule = {
    # Data collection tasks
    "collect-hackernews-hourly": {
        "task": "app.tasks.data_collection.collect_from_source",
        "schedule": crontab(minute=0),  # Every hour
        "args": ("hackernews",),
    },
    "collect-reddit-every-30min": {
        "task": "app.tasks.data_collection.collect_from_source", 
        "schedule": crontab(minute="*/30"),  # Every 30 minutes
        "args": ("reddit",),
    },
    
    # Content processing
    "process-collected-content": {
        "task": "app.tasks.content_processing.process_pending_content",
        "schedule": crontab(minute="*/15"),  # Every 15 minutes
    },
    
    # Publishing tasks
    "auto-publish-content": {
        "task": "app.tasks.publishing.auto_publish_approved_content",
        "schedule": crontab(minute="*/20"),  # Every 20 minutes
    },
    
    # Cleanup tasks
    "cleanup-old-content": {
        "task": "app.tasks.data_collection.cleanup_old_content",
        "schedule": crontab(hour=2, minute=0),  # Daily at 2 AM
    },
}

celery_app.conf.timezone = "UTC"