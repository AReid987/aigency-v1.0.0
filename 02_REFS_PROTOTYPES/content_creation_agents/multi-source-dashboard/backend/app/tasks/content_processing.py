from celery import current_task
from sqlalchemy import select
from datetime import datetime
from typing import List

from app.tasks.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.models.content import Content, ContentStatus

@celery_app.task(bind=True)
async def process_pending_content(self):
    """Process collected content for sentiment analysis and categorization"""
    try:
        current_task.update_state(state="PROGRESS", meta={"status": "Processing content"})
        
        async with AsyncSessionLocal() as db:
            # Get content that needs processing
            result = await db.execute(
                select(Content).where(Content.status == ContentStatus.COLLECTED).limit(50)
            )
            pending_content = result.scalars().all()
            
            processed_count = 0
            
            for content in pending_content:
                try:
                    # Basic content processing
                    content.summary = _generate_summary(content.content or content.title)
                    content.keywords = _extract_keywords(content.title, content.content)
                    content.sentiment_score = _analyze_sentiment(content.title, content.content)
                    content.categories = _categorize_content(content.title, content.content)
                    
                    content.status = ContentStatus.PROCESSED
                    content.processed_at = datetime.utcnow()
                    processed_count += 1
                    
                except Exception as e:
                    print(f"Error processing content {content.id}: {e}")
                    continue
            
            await db.commit()
            
            return {
                "status": "success",
                "processed": processed_count,
                "timestamp": datetime.utcnow().isoformat()
            }
            
    except Exception as e:
        current_task.update_state(state="FAILURE", meta={"error": str(e)})
        raise

def _generate_summary(text: str) -> str:
    """Generate a simple summary of the content"""
    if not text:
        return ""
    
    # Simple summary: first 150 characters
    return text[:150] + "..." if len(text) > 150 else text

def _extract_keywords(title: str, content: str) -> List[str]:
    """Extract keywords from title and content"""
    import re
    
    text = f"{title} {content or ''}"
    # Simple keyword extraction
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    
    # Common tech keywords
    tech_keywords = [
        "python", "javascript", "react", "vue", "angular", "node", "api", "database",
        "machine learning", "ai", "artificial intelligence", "blockchain", "cloud",
        "aws", "docker", "kubernetes", "microservices", "devops", "programming",
        "software", "development", "coding", "algorithm", "data", "analytics"
    ]
    
    found_keywords = []
    for keyword in tech_keywords:
        if keyword in text.lower():
            found_keywords.append(keyword)
    
    # Add frequent words
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    frequent_words = [word for word, freq in word_freq.items() if freq > 1 and len(word) > 4]
    found_keywords.extend(frequent_words[:5])
    
    return list(set(found_keywords))[:10]  # Return top 10 unique keywords

def _analyze_sentiment(title: str, content: str) -> float:
    """Simple sentiment analysis"""
    text = f"{title} {content or ''}".lower()
    
    positive_words = ["good", "great", "excellent", "amazing", "awesome", "love", "best", "perfect", "wonderful"]
    negative_words = ["bad", "terrible", "awful", "hate", "worst", "horrible", "disappointing", "failed"]
    
    positive_count = sum(1 for word in positive_words if word in text)
    negative_count = sum(1 for word in negative_words if word in text)
    
    total_words = len(text.split())
    if total_words == 0:
        return 0.0
    
    # Simple sentiment score between -1 and 1
    sentiment = (positive_count - negative_count) / max(total_words / 10, 1)
    return max(-1.0, min(1.0, sentiment))

def _categorize_content(title: str, content: str) -> List[str]:
    """Categorize content based on keywords"""
    text = f"{title} {content or ''}".lower()
    
    categories = {
        "technology": ["tech", "software", "programming", "code", "development", "api", "framework"],
        "ai_ml": ["ai", "machine learning", "neural", "algorithm", "data science", "tensorflow", "pytorch"],
        "web_development": ["javascript", "react", "vue", "angular", "css", "html", "frontend", "backend"],
        "mobile": ["ios", "android", "mobile", "app", "flutter", "react native"],
        "devops": ["docker", "kubernetes", "aws", "cloud", "deployment", "ci/cd", "infrastructure"],
        "data": ["database", "sql", "nosql", "analytics", "big data", "visualization"],
        "security": ["security", "cybersecurity", "encryption", "authentication", "vulnerability"],
        "startup": ["startup", "entrepreneur", "funding", "venture capital", "business", "company"]
    }
    
    found_categories = []
    for category, keywords in categories.items():
        if any(keyword in text for keyword in keywords):
            found_categories.append(category)
    
    return found_categories[:3]  # Return top 3 categories