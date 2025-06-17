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
        yt = YouTube(url)
        
        # Get video details
        info = {
            "title": yt.title,
            "author": yt.author,
            "channel_name": yt.author,
            "published_date": yt.publish_date,
            "duration": yt.length,
            "view_count": yt.views,
            "video_id": yt.video_id,
            "url": url,
        }
        
        # Try to get transcript
        try:
            captions = yt.captions.get_by_language_code('en')
            if captions:
                info["transcript"] = captions.generate_srt_captions()
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
