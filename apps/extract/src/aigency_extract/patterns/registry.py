"""Registry of extraction patterns."""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

from aigency_extract.data.models import ContentType, ExtractionPattern

# Base patterns
BASE_PATTERNS: Dict[str, ExtractionPattern] = {
    "youtube_summary": ExtractionPattern(
        name="youtube_summary",
        description="Extract key information from YouTube videos with timestamps and quotes",
        prompt_template="""
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
            
            Additional instructions for YouTube content:
            - Focus on the spoken content rather than visuals
            - Note any demonstrations or visual examples mentioned
            - Include timestamps for particularly important moments if available
            - Consider the presenter's emphasis and tone
        """,
        source="fabric",
    ),
    
    "extract_wisdom": ExtractionPattern(
        name="extract_wisdom",
        description="Extract wisdom, insights, and practical knowledge",
        prompt_template="""
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
        source="fabric",
    ),
    
    "summarize": ExtractionPattern(
        name="summarize",
        description="Create comprehensive yet concise summaries",
        prompt_template="""
            Provide a comprehensive yet concise summary of this content.
            Capture the essential information while eliminating redundancy.
            Include:
            1. A thorough summary (3-4 paragraphs)
            2. Key points and arguments
            3. Main conclusions or findings
            4. Important details worth remembering
            5. Context and significance
        """,
        source="fabric",
    ),
    
    "extract_insights": ExtractionPattern(
        name="extract_insights",
        description="Focus on novel ideas and unexpected connections",
        prompt_template="""
            Extract the most valuable insights from this content.
            Focus on novel ideas, unexpected connections, and practical knowledge.
            Include:
            1. A brief overview of the content (1-2 paragraphs)
            2. 7-10 specific insights, ranked by importance
            3. Connections to broader themes or fields
            4. Contrarian or non-obvious points
            5. Practical applications of these insights
        """,
        source="fabric",
    ),
    
    "extract_main_idea": ExtractionPattern(
        name="extract_main_idea",
        description="Identify and explain the central thesis",
        prompt_template="""
            Identify and explain the main idea or central thesis of this content.
            Cut through the details to find the core message.
            Include:
            1. The central thesis stated clearly and concisely (1 paragraph)
            2. 3-5 supporting arguments or points
            3. Evidence presented for this main idea
            4. Context needed to understand the significance
            5. Implications of this main idea
        """,
        source="fabric",
    ),
    
    "create_5_sentence_summary": ExtractionPattern(
        name="create_5_sentence_summary",
        description="Summarize the entire content in exactly 5 sentences",
        prompt_template="""
            Summarize this entire content in exactly 5 sentences.
            Each sentence should capture a critical aspect:
            1. The overall topic and scope
            2. The main argument or thesis
            3. The key evidence or examples
            4. The most important finding or conclusion
            5. The significance or implications
        """,
        source="fabric",
    ),
    
    "create_logo": ExtractionPattern(
        name="create_logo",
        description="Generate logo ideas and descriptions",
        prompt_template="""
            Create detailed logo concepts based on the provided information.
            For each logo concept, include:
            1. A clear description of the visual elements
            2. Color palette recommendations with hex codes
            3. Typography suggestions
            4. Symbolic meaning of the design elements
            5. How the logo represents the brand's values
            6. Variations for different contexts (web, print, mobile)
            
            Generate 3 distinct logo concepts that are:
            - Memorable and distinctive
            - Scalable and versatile
            - Appropriate for the brand/product
            - Timeless rather than trendy
        """,
        source="fabric",
    ),
    
    "improve_art_prompt": ExtractionPattern(
        name="improve_art_prompt",
        description="Enhance prompts for image generation",
        prompt_template="""
            Improve the provided art generation prompt to create more detailed, 
            vivid, and effective results with AI image generators.
            
            For the improved prompt, include:
            1. Detailed subject description with specific attributes
            2. Setting/environment details with atmosphere
            3. Lighting conditions and color palette
            4. Artistic style, medium, and influences
            5. Composition, perspective, and framing
            6. Technical parameters (aspect ratio, quality modifiers)
            7. Negative prompts (what to avoid)
            
            Format the improved prompt in a way that's optimized for:
            - Clarity and specificity
            - Visual coherence
            - Technical compatibility with image generation AI
            - Achieving the intended artistic vision
        """,
        source="fabric",
    ),
    
    "suggest_pattern": ExtractionPattern(
        name="suggest_pattern",
        description="Suggest the best extraction pattern for a given content",
        prompt_template="""
            Analyze the provided content and suggest the most appropriate extraction pattern to use.
            Consider the content type, structure, purpose, and what insights would be most valuable to extract.
            
            Available patterns:
            - youtube_summary: Extract key information from YouTube videos with timestamps and quotes
            - extract_wisdom: Extract wisdom, insights, and practical knowledge
            - summarize: Create comprehensive yet concise summaries
            - extract_insights: Focus on novel ideas and unexpected connections
            - extract_main_idea: Identify and explain the central thesis
            - create_5_sentence_summary: Summarize the entire content in exactly 5 sentences
            - create_logo: Generate logo ideas and descriptions
            - improve_art_prompt: Enhance prompts for image generation
            
            Provide:
            1. The recommended pattern name
            2. A brief explanation of why this pattern is most appropriate
            3. Any specific modifications to the pattern that might be helpful
        """,
        source="custom",
    ),
}


class PatternRegistry:
    """Registry for extraction patterns."""

    def __init__(self):
        """Initialize the pattern registry."""
        self.patterns: Dict[str, ExtractionPattern] = {}
        self._load_base_patterns()
        self._load_custom_patterns()

    def _load_base_patterns(self):
        """Load base patterns."""
        self.patterns.update(BASE_PATTERNS)

    def _load_custom_patterns(self):
        """Load custom patterns from file."""
        # Get user's home directory
        home_dir = Path.home()
        custom_patterns_dir = home_dir / ".aigency_extract" / "patterns"
        
        # Create directory if it doesn't exist
        custom_patterns_dir.mkdir(parents=True, exist_ok=True)
        
        # Load custom patterns
        custom_patterns_file = custom_patterns_dir / "custom_patterns.json"
        if custom_patterns_file.exists():
            try:
                with open(custom_patterns_file, "r") as f:
                    custom_patterns = json.load(f)
                
                for pattern_data in custom_patterns:
                    pattern = ExtractionPattern(**pattern_data)
                    self.patterns[pattern.name] = pattern
            except Exception:
                # If loading fails, just continue with base patterns
                pass

    def get_pattern(self, pattern_name: str) -> Optional[ExtractionPattern]:
        """Get a pattern by name."""
        return self.patterns.get(pattern_name)

    def get_all_patterns(self) -> List[ExtractionPattern]:
        """Get all patterns."""
        return list(self.patterns.values())

    def get_pattern_names(self) -> List[str]:
        """Get all pattern names."""
        return list(self.patterns.keys())

    def add_pattern(self, pattern: ExtractionPattern) -> None:
        """Add a new pattern."""
        self.patterns[pattern.name] = pattern
        self._save_custom_patterns()

    def remove_pattern(self, pattern_name: str) -> bool:
        """Remove a pattern."""
        if pattern_name in BASE_PATTERNS:
            return False  # Can't remove base patterns
        
        if pattern_name in self.patterns:
            del self.patterns[pattern_name]
            self._save_custom_patterns()
            return True
        
        return False

    def _save_custom_patterns(self):
        """Save custom patterns to file."""
        # Get user's home directory
        home_dir = Path.home()
        custom_patterns_dir = home_dir / ".aigency_extract" / "patterns"
        
        # Create directory if it doesn't exist
        custom_patterns_dir.mkdir(parents=True, exist_ok=True)
        
        # Save custom patterns
        custom_patterns = []
        for pattern_name, pattern in self.patterns.items():
            if pattern_name not in BASE_PATTERNS:
                custom_patterns.append(pattern.model_dump())
        
        custom_patterns_file = custom_patterns_dir / "custom_patterns.json"
        with open(custom_patterns_file, "w") as f:
            json.dump(custom_patterns, f, indent=2)


# Singleton instance
pattern_registry = PatternRegistry()


def get_pattern(pattern_name: str) -> Optional[ExtractionPattern]:
    """Get a pattern by name."""
    return pattern_registry.get_pattern(pattern_name)


def get_all_patterns() -> List[ExtractionPattern]:
    """Get all patterns."""
    return pattern_registry.get_all_patterns()


def get_pattern_names() -> List[str]:
    """Get all pattern names."""
    return pattern_registry.get_pattern_names()


def add_pattern(pattern: ExtractionPattern) -> None:
    """Add a new pattern."""
    pattern_registry.add_pattern(pattern)


def remove_pattern(pattern_name: str) -> bool:
    """Remove a pattern."""
    return pattern_registry.remove_pattern(pattern_name)
