"""Database operations for storing and retrieving extracted content."""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

from sqlite_utils import Database

from aigency_extract.data.models import ArticleContent, Content, ContentType, YouTubeContent


class ExtractDatabase:
    """Database manager for extracted content."""

    def __init__(self, db_path: Optional[str] = None):
        """Initialize the database connection."""
        if db_path is None:
            # Create default database in user's home directory
            home_dir = Path.home()
            data_dir = home_dir / ".aigency_extract"
            data_dir.mkdir(exist_ok=True)
            db_path = str(data_dir / "extracts.db")
        
        self.db_path = db_path
        self.db = Database(db_path)
        self._initialize_tables()
    
    def _initialize_tables(self):
        """Create tables if they don't exist."""
        # Content table
        if "content" not in self.db.table_names():
            self.db.create_table(
                "content",
                {
                    "id": int,
                    "title": str,
                    "url": str,
                    "content_type": str,
                    "extracted_at": str,
                    "author": str,
                    "published_date": str,
                    "duration": int,
                    "summary": str,
                    "key_insights": str,  # JSON list
                    "main_points": str,  # JSON list
                    "quotes": str,  # JSON list
                    "questions_raised": str,  # JSON list
                    "action_items": str,  # JSON list
                    "extraction_pattern": str,
                    "extraction_quality": float,
                    "notes": str,
                },
                pk="id",
            )
            self.db["content"].create_index(["content_type"])
            self.db["content"].create_index(["url"])
        
        # YouTube specific table
        if "youtube_content" not in self.db.table_names():
            self.db.create_table(
                "youtube_content",
                {
                    "content_id": int,
                    "video_id": str,
                    "channel_name": str,
                    "view_count": int,
                    "like_count": int,
                    "transcript": str,
                },
                pk="content_id",
                foreign_keys=[("content_id", "content", "id")],
            )
            self.db["youtube_content"].create_index(["video_id"])
        
        # Article specific table
        if "article_content" not in self.db.table_names():
            self.db.create_table(
                "article_content",
                {
                    "content_id": int,
                    "domain": str,
                    "word_count": int,
                    "html_content": str,
                },
                pk="content_id",
                foreign_keys=[("content_id", "content", "id")],
            )
            self.db["article_content"].create_index(["domain"])
        
        # Tags table
        if "tags" not in self.db.table_names():
            self.db.create_table(
                "tags",
                {
                    "id": int,
                    "name": str,
                },
                pk="id",
            )
            self.db["tags"].create_index(["name"], unique=True)
        
        # Content-Tags relationship table
        if "content_tags" not in self.db.table_names():
            self.db.create_table(
                "content_tags",
                {
                    "content_id": int,
                    "tag_id": int,
                },
                foreign_keys=[
                    ("content_id", "content", "id"),
                    ("tag_id", "tags", "id"),
                ],
            )
            self.db["content_tags"].create_index(["content_id", "tag_id"], unique=True)
    
    def save_content(self, content: Union[Content, YouTubeContent, ArticleContent]) -> int:
        """Save content to the database."""
        # Convert lists to JSON strings
        content_dict = content.model_dump()
        
        # Extract tags before removing from dict
        tags = content_dict.pop("tags", [])
        
        for field in ["key_insights", "main_points", "quotes", "questions_raised", "action_items"]:
            if field in content_dict and isinstance(content_dict[field], list):
                content_dict[field] = json.dumps(content_dict[field])
        
        # Handle datetime objects
        for field in ["extracted_at", "published_date"]:
            if field in content_dict and content_dict[field] is not None:
                if isinstance(content_dict[field], datetime):
                    content_dict[field] = content_dict[field].isoformat()
        
        # Remove id if None
        if "id" in content_dict and content_dict["id"] is None:
            content_dict.pop("id")
        
        # Insert into content table
        content_id = self.db["content"].insert(
            {k: v for k, v in content_dict.items() if k not in ["video_id", "channel_name", "view_count", "like_count", "transcript", "domain", "word_count", "html_content"]},
            pk="id",
            replace=True,
        ).last_pk
        
        # Insert into specific content type table
        if content.content_type == ContentType.YOUTUBE:
            youtube_dict = {
                "content_id": content_id,
                "video_id": content_dict.get("video_id"),
                "channel_name": content_dict.get("channel_name"),
                "view_count": content_dict.get("view_count"),
                "like_count": content_dict.get("like_count"),
                "transcript": content_dict.get("transcript"),
            }
            self.db["youtube_content"].insert(youtube_dict, pk="content_id", replace=True)
        
        elif content.content_type == ContentType.ARTICLE:
            article_dict = {
                "content_id": content_id,
                "domain": content_dict.get("domain"),
                "word_count": content_dict.get("word_count"),
                "html_content": content_dict.get("html_content"),
            }
            self.db["article_content"].insert(article_dict, pk="content_id", replace=True)
        
        # Handle tags
        self._save_tags(content_id, tags)
        
        return content_id
    
    def _save_tags(self, content_id: int, tags: List[str]):
        """Save tags for a content item."""
        # First, remove existing tags for this content
        self.db.execute("DELETE FROM content_tags WHERE content_id = ?", [content_id])
        
        # Then add new tags
        for tag_name in tags:
            # Get or create tag
            tag_id = self._get_or_create_tag(tag_name)
            
            # Link tag to content
            self.db["content_tags"].insert(
                {"content_id": content_id, "tag_id": tag_id},
                ignore=True,
            )
    
    def _get_or_create_tag(self, tag_name: str) -> int:
        """Get a tag ID or create it if it doesn't exist."""
        tag = self.db.execute("SELECT id FROM tags WHERE name = ?", [tag_name]).fetchone()
        if tag:
            return tag["id"]
        
        return self.db["tags"].insert({"name": tag_name}).last_pk
    
    def get_content(self, content_id: int) -> Optional[Union[Content, YouTubeContent, ArticleContent]]:
        """Get content by ID."""
        content_row = self.db.execute(
            "SELECT * FROM content WHERE id = ?", [content_id]
        ).fetchone()
        
        if not content_row:
            return None
        
        return self._row_to_content(content_row)
    
    def get_content_by_url(self, url: str) -> Optional[Union[Content, YouTubeContent, ArticleContent]]:
        """Get content by URL."""
        content_row = self.db.execute(
            "SELECT * FROM content WHERE url = ?", [url]
        ).fetchone()
        
        if not content_row:
            return None
        
        return self._row_to_content(content_row)
    
    def search_content(
        self, 
        query: str = "", 
        content_type: Optional[ContentType] = None,
        tag: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Union[Content, YouTubeContent, ArticleContent]]:
        """Search for content."""
        sql = "SELECT c.* FROM content c"
        params = []
        
        # Join with tags if needed
        if tag:
            sql += " JOIN content_tags ct ON c.id = ct.content_id JOIN tags t ON ct.tag_id = t.id"
        
        # Build WHERE clause
        where_clauses = []
        
        if query:
            where_clauses.append("(c.title LIKE ? OR c.summary LIKE ?)")
            params.extend([f"%{query}%", f"%{query}%"])
        
        if content_type:
            where_clauses.append("c.content_type = ?")
            params.append(content_type)
        
        if tag:
            where_clauses.append("t.name = ?")
            params.append(tag)
        
        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)
        
        # Add limit and offset
        sql += " ORDER BY c.extracted_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        # Execute query
        rows = self.db.execute(sql, params).fetchall()
        
        # Convert rows to content objects
        return [self._row_to_content(row) for row in rows]
    
    def _row_to_content(self, row: Dict) -> Union[Content, YouTubeContent, ArticleContent]:
        """Convert a database row to a content object."""
        # Convert row to dict
        content_dict = dict(row)
        
        # Parse JSON fields
        for field in ["key_insights", "main_points", "quotes", "questions_raised", "action_items"]:
            if content_dict.get(field):
                content_dict[field] = json.loads(content_dict[field])
            else:
                content_dict[field] = []
        
        # Get content type
        content_type = ContentType(content_dict["content_type"])
        
        # Get tags
        tags = self.db.execute(
            "SELECT t.name FROM tags t JOIN content_tags ct ON t.id = ct.tag_id WHERE ct.content_id = ?",
            [content_dict["id"]]
        ).fetchall()
        content_dict["tags"] = [tag["name"] for tag in tags]
        
        # Get type-specific data
        if content_type == ContentType.YOUTUBE:
            youtube_row = self.db.execute(
                "SELECT * FROM youtube_content WHERE content_id = ?", [content_dict["id"]]
            ).fetchone()
            if youtube_row:
                content_dict.update(dict(youtube_row))
            return YouTubeContent(**content_dict)
        
        elif content_type == ContentType.ARTICLE:
            article_row = self.db.execute(
                "SELECT * FROM article_content WHERE content_id = ?", [content_dict["id"]]
            ).fetchone()
            if article_row:
                content_dict.update(dict(article_row))
            return ArticleContent(**content_dict)
        
        return Content(**content_dict)
    
    def get_all_tags(self) -> List[str]:
        """Get all tags in the database."""
        rows = self.db.execute("SELECT name FROM tags ORDER BY name").fetchall()
        return [row["name"] for row in rows]
    
    def get_stats(self) -> Dict:
        """Get database statistics."""
        return {
            "total_content": self.db.execute("SELECT COUNT(*) as count FROM content").fetchone()["count"],
            "youtube_videos": self.db.execute("SELECT COUNT(*) as count FROM content WHERE content_type = ?", [ContentType.YOUTUBE]).fetchone()["count"],
            "articles": self.db.execute("SELECT COUNT(*) as count FROM content WHERE content_type = ?", [ContentType.ARTICLE]).fetchone()["count"],
            "other": self.db.execute("SELECT COUNT(*) as count FROM content WHERE content_type = ?", [ContentType.OTHER]).fetchone()["count"],
            "total_tags": self.db.execute("SELECT COUNT(*) as count FROM tags").fetchone()["count"],
        }
