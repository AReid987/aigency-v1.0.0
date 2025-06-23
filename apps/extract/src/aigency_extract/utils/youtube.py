"""YouTube video extraction utilities."""

import re
from typing import Dict, Optional, Tuple

import pytube
from pytube import YouTube

from aigency_extract.data.models import LLMProvider, YouTubeContent


def extract_video_id(url: str) -> Optional[str]:
    """Extract YouTube video ID from URL."""
    # Regular expressions for different YouTube URL formats
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",  # Standard YouTube URLs
        r"(?:embed\/)([0-9A-Za-z_-]{11})",  # Embedded URLs
        r"(?:shorts\/)([0-9A-Za-z_-]{11})",  # Shorts URLs
        r"^([0-9A-Za-z_-]{11})$",  # Just the ID
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def get_video_info(url: str) -> Dict:
    """Get information about a YouTube video."""
    try:
        video_id = extract_video_id(url)
        if not video_id:
            raise ValueError("Invalid YouTube URL")
            
        # Use direct HTML scraping to get video metadata
        import requests
        from bs4 import BeautifulSoup
        
        # Fetch video page
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(f"https://www.youtube.com/watch?v={video_id}", headers=headers)
        response.raise_for_status()
        
        # Parse HTML to extract metadata
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title with fallback
        title_tag = soup.find("meta", property="og:title")
        title = title_tag["content"] if title_tag else "Unknown Title"
        
        # Extract channel name with fallback
        channel_tag = soup.find("link", itemprop="name")
        channel_name = channel_tag["content"] if channel_tag else "Unknown Channel"
        
        # Extract view count with fallback
        view_tag = soup.find("meta", itemprop="interactionCount")
        view_count = view_tag["content"] if view_tag else "0"
        
        # Create info dictionary
        info = {
            "title": title,
            "author": channel_name,
            "channel_name": channel_name,
            "published_date": None,  # Not available in this method
            "duration": None,  # Not available in this method
            "view_count": view_count,
            "video_id": video_id,
            "url": url,
        }
        
        # Try to get transcript using youtube_transcript_api
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            info["transcript"] = "\n".join([entry['text'] for entry in transcript])
        except Exception:
            # If transcript extraction fails, continue without it
            pass
        
        return info
    
    except Exception as e:
        raise ValueError(f"Failed to extract video info: {str(e)}")



def create_youtube_content_shell(
    url: str,
    provider: LLMProvider = LLMProvider.MISTRAL,
    model: str = "mistral-large-latest",
) -> YouTubeContent:
    """Create a YouTubeContent object with basic info from a URL."""
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError(f"Invalid YouTube URL: {url}")
    
    video_info = get_video_info(url)
    
    return YouTubeContent(
        title=video_info.get("title", "Unknown Title"),
        url=url,
        video_id=video_id,
        channel_name=video_info.get("channel_name"),
        author=video_info.get("author"),
        published_date=video_info.get("published_date"),
        duration=video_info.get("duration"),
        view_count=video_info.get("view_count"),
        transcript=video_info.get("transcript"),
        summary="",  # Will be filled by extraction process
        extraction_pattern="",  # Will be filled by extraction process
        extraction_provider=provider,
        extraction_model=model,
    )
