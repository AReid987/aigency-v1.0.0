"""Content extraction utilities using patterns."""

import os
import re
from typing import Dict, List, Optional, Union

from aigency_extract.data.models import (ArticleContent, Content, ContentType,
                                        LLMProvider, YouTubeContent)
from aigency_extract.llm import get_llm
from aigency_extract.patterns.registry import get_pattern


class ContentExtractor:
    """Extract content using AI."""
    
    def __init__(
        self, 
        provider_name: Optional[str] = None,
        model_name: Optional[str] = None
    ):
        """Initialize the extractor with an LLM provider."""
        self.llm = get_llm(provider_name, model_name)
    
    def extract_content(
        self, 
        content: Union[YouTubeContent, ArticleContent], 
        pattern_name: str
    ) -> Union[YouTubeContent, ArticleContent]:
        """Extract insights from content using the specified pattern."""
        # Get the pattern
        pattern = get_pattern(pattern_name)
        if not pattern:
            raise ValueError(f"Pattern '{pattern_name}' not found")
        
        # Prepare the content for extraction
        if content.content_type == ContentType.YOUTUBE:
            input_text = self._prepare_youtube_content(content)
        elif content.content_type == ContentType.ARTICLE:
            input_text = self._prepare_article_content(content)
        else:
            raise ValueError(f"Unsupported content type: {content.content_type}")
        
        # Get the prompt for the pattern
        prompt = pattern.prompt_template
        
        # Call the LLM
        response = self.llm.complete(
            prompt=input_text,
            system_prompt=prompt,
            temperature=0.3,
            max_tokens=2000,
        )
        
        # Store the raw extraction
        content.raw_extraction = response
        
        # Parse the response
        extracted_content = self._parse_extraction_response(response)
        
        # Update the content object
        content.summary = extracted_content.get("summary", "")
        content.key_insights = extracted_content.get("key_insights", [])
        content.main_points = extracted_content.get("main_points", [])
        content.quotes = extracted_content.get("quotes", [])
        content.questions_raised = extracted_content.get("questions_raised", [])
        content.action_items = extracted_content.get("action_items", [])
        content.extraction_pattern = pattern_name
        content.extraction_provider = self.llm.provider_name
        content.extraction_model = self.llm.default_model if hasattr(self.llm, "default_model") else "unknown"
        
        # Generate tags
        content.tags = self._generate_tags(content)
        
        return content
    
    def _prepare_youtube_content(self, content: YouTubeContent) -> str:
        """Prepare YouTube content for extraction."""
        parts = [
            f"Title: {content.title}",
            f"Channel: {content.channel_name}" if content.channel_name else "",
            f"Duration: {self._format_duration(content.duration)}" if content.duration else "",
        ]
        
        # Add transcript if available
        if content.transcript:
            parts.append("\nTranscript:")
            parts.append(content.transcript[:50000])  # Limit transcript length
        
        return "\n".join(filter(None, parts))
    
    def _prepare_article_content(self, content: ArticleContent) -> str:
        """Prepare article content for extraction."""
        parts = [
            f"Title: {content.title}",
            f"Author: {content.author}" if content.author else "",
            f"Source: {content.domain}" if content.domain else "",
        ]
        
        # Extract text from HTML if available
        if content.html_content:
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(content.html_content, "html.parser")
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.extract()
                
                # Get text
                text = soup.get_text()
                
                # Break into lines and remove leading and trailing space
                lines = (line.strip() for line in text.splitlines())
                # Break multi-headlines into a line each
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                # Drop blank lines
                text = '\n'.join(chunk for chunk in chunks if chunk)
                
                parts.append("\nContent:")
                parts.append(text[:50000])  # Limit content length
            except Exception:
                # If HTML parsing fails, just use the raw HTML
                parts.append("\nContent:")
                parts.append(content.html_content[:50000])
        
        return "\n".join(filter(None, parts))
    
    def _parse_extraction_response(self, response: str) -> Dict:
        """Parse the extraction response into structured data."""
        result = {
            "summary": "",
            "key_insights": [],
            "main_points": [],
            "quotes": [],
            "questions_raised": [],
            "action_items": [],
        }
        
        # Simple parsing based on headings
        current_section = "summary"
        lines = response.split("\n")
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for section headers
            lower_line = line.lower()
            if any(keyword in lower_line for keyword in ["key insight", "insight", "insights"]):
                current_section = "key_insights"
                continue
            elif any(keyword in lower_line for keyword in ["main point", "key point", "main points"]):
                current_section = "main_points"
                continue
            elif "quote" in lower_line or "notable quote" in lower_line:
                current_section = "quotes"
                continue
            elif "question" in lower_line:
                current_section = "questions_raised"
                continue
            elif any(keyword in lower_line for keyword in ["action item", "next step", "takeaway"]):
                current_section = "action_items"
                continue
            elif "summary" in lower_line and not result["summary"]:
                current_section = "summary"
                continue
            
            # Process line based on current section
            if current_section == "summary":
                if result["summary"]:
                    result["summary"] += "\n" + line
                else:
                    result["summary"] = line
            else:
                # Clean up bullet points and numbering
                clean_line = re.sub(r"^\d+\.\s*|\*\s*|-\s*", "", line).strip()
                if clean_line:
                    result[current_section].append(clean_line)
        
        return result
    
    def _generate_tags(self, content: Union[YouTubeContent, ArticleContent]) -> List[str]:
        """Generate tags for the content based on extracted information."""
        # Combine all text fields for tag generation
        text = f"{content.title} {content.summary} {' '.join(content.key_insights)}"
        
        try:
            response = self.llm.complete(
                prompt=text[:2000],  # Limit input size
                system_prompt="Generate 5-7 relevant tags for this content. Each tag should be a single word or short phrase. Return the tags as a comma-separated list without numbering or bullets.",
                temperature=0.3,
                max_tokens=100,
            )
            
            # Split by commas and clean up
            tags = [tag.strip() for tag in response.split(",")]
            # Remove any empty tags or tags with special characters
            tags = [tag for tag in tags if tag and re.match(r"^[a-zA-Z0-9\s\-_]+$", tag)]
            # Limit to 7 tags
            return tags[:7]
        
        except Exception:
            # If tag generation fails, return empty list
            return []
    
    @staticmethod
    def _format_duration(seconds: int) -> str:
        """Format duration in seconds to HH:MM:SS format."""
        if not seconds:
            return ""
        
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
