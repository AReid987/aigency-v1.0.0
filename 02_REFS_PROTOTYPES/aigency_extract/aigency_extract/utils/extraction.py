"""Content extraction utilities using Fabric patterns."""

import os
from typing import Dict, List, Optional, Union

import openai
from openai import OpenAI

from aigency_extract.data.models import ArticleContent, Content, ContentType, YouTubeContent


class ExtractionPatterns:
    """Extraction patterns inspired by Fabric."""
    
    YOUTUBE_SUMMARY = "youtube_summary"
    EXTRACT_WISDOM = "extract_wisdom"
    SUMMARIZE = "summarize"
    EXTRACT_INSIGHTS = "extract_insights"
    EXTRACT_MAIN_IDEA = "extract_main_idea"
    CREATE_5_SENTENCE_SUMMARY = "create_5_sentence_summary"
    
    @classmethod
    def get_pattern_prompt(cls, pattern_name: str, content_type: ContentType) -> str:
        """Get the prompt for a specific pattern."""
        base_prompts = {
            cls.YOUTUBE_SUMMARY: """
                Extract the most important information from this YouTube video.
                Focus on the key insights, main points, and actionable takeaways.
                Organize the information in a clear, concise manner.
                Include:
                1. A brief summary (2-3 paragraphs)
                2. 5-7 key insights
                3. Main points in bullet form
                4. Notable quotes
                5. Questions raised by the content
                6. Action items or next steps
            """,
            cls.EXTRACT_WISDOM: """
                Extract the wisdom and insights from this content.
                Focus on the most valuable ideas, concepts, and lessons.
                Organize the information in a clear, structured manner.
                Include:
                1. A concise summary of the core message (2-3 paragraphs)
                2. 5-7 key insights or wisdom points
                3. Main arguments or concepts in bullet form
                4. Notable quotes or statements
                5. Questions this content raises or answers
                6. Practical applications or action items
            """,
            cls.SUMMARIZE: """
                Provide a comprehensive yet concise summary of this content.
                Capture the essential information while eliminating redundancy.
                Include:
                1. A thorough summary (3-4 paragraphs)
                2. Key points and arguments
                3. Main conclusions or findings
                4. Important details worth remembering
                5. Context and significance
            """,
            cls.EXTRACT_INSIGHTS: """
                Extract the most valuable insights from this content.
                Focus on novel ideas, unexpected connections, and practical knowledge.
                Include:
                1. A brief overview of the content (1-2 paragraphs)
                2. 7-10 specific insights, ranked by importance
                3. Connections to broader themes or fields
                4. Contrarian or non-obvious points
                5. Practical applications of these insights
            """,
            cls.EXTRACT_MAIN_IDEA: """
                Identify and explain the main idea or central thesis of this content.
                Cut through the details to find the core message.
                Include:
                1. The central thesis stated clearly and concisely (1 paragraph)
                2. 3-5 supporting arguments or points
                3. Evidence presented for this main idea
                4. Context needed to understand the significance
                5. Implications of this main idea
            """,
            cls.CREATE_5_SENTENCE_SUMMARY: """
                Summarize this entire content in exactly 5 sentences.
                Each sentence should capture a critical aspect:
                1. The overall topic and scope
                2. The main argument or thesis
                3. The key evidence or examples
                4. The most important finding or conclusion
                5. The significance or implications
            """,
        }
        
        # Get base prompt
        prompt = base_prompts.get(pattern_name, base_prompts[cls.EXTRACT_WISDOM])
        
        # Add content-specific instructions
        if content_type == ContentType.YOUTUBE:
            prompt += """
                Additional instructions for YouTube content:
                - Focus on the spoken content rather than visuals
                - Note any demonstrations or visual examples mentioned
                - Include timestamps for particularly important moments if available
                - Consider the presenter's emphasis and tone
            """
        elif content_type == ContentType.ARTICLE:
            prompt += """
                Additional instructions for article content:
                - Pay attention to the article's structure and headings
                - Note any data, statistics, or research cited
                - Consider the author's perspective and potential biases
                - Identify the intended audience and purpose
            """
        
        return prompt.strip()
    
    @classmethod
    def get_all_patterns(cls) -> List[str]:
        """Get all available extraction patterns."""
        return [
            cls.YOUTUBE_SUMMARY,
            cls.EXTRACT_WISDOM,
            cls.SUMMARIZE,
            cls.EXTRACT_INSIGHTS,
            cls.EXTRACT_MAIN_IDEA,
            cls.CREATE_5_SENTENCE_SUMMARY,
        ]


class ContentExtractor:
    """Extract content using AI."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the extractor with an OpenAI API key."""
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it to the constructor.")
        
        self.client = OpenAI(api_key=self.api_key)
    
    def extract_content(
        self, 
        content: Union[YouTubeContent, ArticleContent], 
        pattern: str = ExtractionPatterns.EXTRACT_WISDOM
    ) -> Union[YouTubeContent, ArticleContent]:
        """Extract insights from content using the specified pattern."""
        # Prepare the content for extraction
        if content.content_type == ContentType.YOUTUBE:
            input_text = self._prepare_youtube_content(content)
        elif content.content_type == ContentType.ARTICLE:
            input_text = self._prepare_article_content(content)
        else:
            raise ValueError(f"Unsupported content type: {content.content_type}")
        
        # Get the prompt for the pattern
        prompt = ExtractionPatterns.get_pattern_prompt(pattern, content.content_type)
        
        # Call the OpenAI API
        response = self._call_openai_api(input_text, prompt)
        
        # Parse the response
        extracted_content = self._parse_extraction_response(response)
        
        # Update the content object
        content.summary = extracted_content.get("summary", "")
        content.key_insights = extracted_content.get("key_insights", [])
        content.main_points = extracted_content.get("main_points", [])
        content.quotes = extracted_content.get("quotes", [])
        content.questions_raised = extracted_content.get("questions_raised", [])
        content.action_items = extracted_content.get("action_items", [])
        content.extraction_pattern = pattern
        
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
    
    def _call_openai_api(self, input_text: str, prompt: str) -> str:
        """Call the OpenAI API to extract content."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Use appropriate model
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": input_text}
                ],
                temperature=0.3,
                max_tokens=2000,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise ValueError(f"OpenAI API call failed: {str(e)}")
    
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
            if "key insight" in lower_line or "insight" in lower_line:
                current_section = "key_insights"
                continue
            elif "main point" in lower_line or "key point" in lower_line:
                current_section = "main_points"
                continue
            elif "quote" in lower_line or "notable quote" in lower_line:
                current_section = "quotes"
                continue
            elif "question" in lower_line:
                current_section = "questions_raised"
                continue
            elif "action item" in lower_line or "next step" in lower_line or "takeaway" in lower_line:
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
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Use a smaller model for tag generation
                messages=[
                    {"role": "system", "content": "Generate 5-7 relevant tags for this content. Each tag should be a single word or short phrase. Return the tags as a comma-separated list without numbering or bullets."},
                    {"role": "user", "content": text[:2000]}  # Limit input size
                ],
                temperature=0.3,
                max_tokens=100,
            )
            
            tags_text = response.choices[0].message.content
            # Split by commas and clean up
            tags = [tag.strip() for tag in tags_text.split(",")]
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
