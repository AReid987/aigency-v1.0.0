#!/usr/bin/env python3
"""
Startup script to initialize the database and seed initial data
"""
import asyncio
import os
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import engine, AsyncSessionLocal
from app.core.database import Base
from app.models.source import Source, SourceType, SourceStatus
from app.models.user import User
from app.auth.security import get_password_hash

async def create_tables():
    """Create all database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created successfully")

async def seed_sources():
    """Seed initial data sources"""
    async with AsyncSessionLocal() as db:
        # Check if sources already exist
        existing_sources = await db.execute("SELECT COUNT(*) FROM sources")
        count = existing_sources.scalar()
        
        if count > 0:
            print("📝 Sources already exist, skipping seed")
            return
        
        # Hacker News source
        hn_source = Source(
            name="hackernews",
            display_name="Hacker News",
            description="Technology news and discussions from Hacker News",
            type=SourceType.FORUM,
            status=SourceStatus.ACTIVE,
            base_url="https://hacker-news.firebaseio.com/v0",
            requires_auth=False,
            rate_limit_per_minute=60,
            config_schema={
                "type": "object",
                "properties": {
                    "story_type": {"type": "string", "enum": ["topstories", "newstories", "beststories"], "default": "topstories"},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 30},
                    "min_score": {"type": "integer", "minimum": 0, "default": 10}
                }
            },
            default_config={"story_type": "topstories", "limit": 30, "min_score": 10},
            endpoints={"stories": "/topstories.json", "item": "/item/{id}.json"}
        )
        
        # Reddit source
        reddit_source = Source(
            name="reddit",
            display_name="Reddit",
            description="Social news aggregation and discussion",
            type=SourceType.SOCIAL,
            status=SourceStatus.ACTIVE,
            base_url="https://oauth.reddit.com",
            requires_auth=True,
            auth_type="oauth2",
            rate_limit_per_minute=100,
            config_schema={
                "type": "object",
                "properties": {
                    "subreddits": {"type": "array", "items": {"type": "string"}, "default": ["programming"]},
                    "sort": {"type": "string", "enum": ["hot", "new", "top"], "default": "hot"},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 25}
                }
            },
            default_config={"subreddits": ["programming", "technology"], "sort": "hot", "limit": 25},
            endpoints={"subreddit": "/r/{subreddit}/{sort}"}
        )
        
        db.add(hn_source)
        db.add(reddit_source)
        await db.commit()
        print("✅ Initial data sources seeded successfully")

async def create_admin_user():
    """Create default admin user"""
    async with AsyncSessionLocal() as db:
        # Check if admin exists
        from sqlalchemy import select
        result = await db.execute(select(User).where(User.email == "admin@dashboard.local"))
        existing_admin = result.scalar_one_or_none()
        
        if existing_admin:
            print("📝 Admin user already exists")
            return
        
        admin_user = User(
            email="admin@dashboard.local",
            username="admin", 
            hashed_password=get_password_hash("admin123"),
            full_name="System Administrator",
            is_active=True,
            is_superuser=True
        )
        
        db.add(admin_user)
        await db.commit()
        print("✅ Admin user created: admin@dashboard.local / admin123")

async def main():
    """Main startup sequence"""
    print("🚀 Starting database initialization...")
    
    try:
        await create_tables()
        await seed_sources()
        await create_admin_user()
        print("\n🎉 Database initialization completed successfully!")
        print("\n📋 Next steps:")
        print("1. Start the backend server: uvicorn app.main:app --reload")
        print("2. Start Celery worker: celery -A app.tasks.celery_app worker --loglevel=info")
        print("3. Start Celery beat: celery -A app.tasks.celery_app beat --loglevel=info")
        print("4. Access API docs at: http://localhost:8000/docs")
        print("5. Login with: admin@dashboard.local / admin123")
        
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())