"""Stitch functionality for chaining patterns together."""

import json
from pathlib import Path
from typing import Dict, List, Optional, Union

from aigency_extract.data.models import (ArticleContent, Content, ContentType,
                                        Stitch, StitchStep, YouTubeContent)
from aigency_extract.patterns.extraction import ContentExtractor


class StitchRegistry:
    """Registry for stitches."""

    def __init__(self):
        """Initialize the stitch registry."""
        self.stitches: Dict[int, Stitch] = {}
        self._load_stitches()

    def _load_stitches(self):
        """Load stitches from file."""
        # Get user's home directory
        home_dir = Path.home()
        stitches_dir = home_dir / ".aigency_extract" / "stitches"
        
        # Create directory if it doesn't exist
        stitches_dir.mkdir(parents=True, exist_ok=True)
        
        # Load stitches
        stitches_file = stitches_dir / "stitches.json"
        if stitches_file.exists():
            try:
                with open(stitches_file, "r") as f:
                    stitches_data = json.load(f)
                
                for stitch_data in stitches_data:
                    stitch = Stitch(**stitch_data)
                    self.stitches[stitch.id or len(self.stitches) + 1] = stitch
            except Exception:
                # If loading fails, just continue with empty registry
                pass

    def get_stitch(self, stitch_id: int) -> Optional[Stitch]:
        """Get a stitch by ID."""
        return self.stitches.get(stitch_id)

    def get_stitch_by_name(self, name: str) -> Optional[Stitch]:
        """Get a stitch by name."""
        for stitch in self.stitches.values():
            if stitch.name == name:
                return stitch
        return None

    def get_all_stitches(self) -> List[Stitch]:
        """Get all stitches."""
        return list(self.stitches.values())

    def add_stitch(self, stitch: Stitch) -> int:
        """Add a new stitch."""
        # Generate ID if not provided
        if stitch.id is None:
            stitch.id = max(self.stitches.keys(), default=0) + 1
        
        self.stitches[stitch.id] = stitch
        self._save_stitches()
        return stitch.id

    def remove_stitch(self, stitch_id: int) -> bool:
        """Remove a stitch."""
        if stitch_id in self.stitches:
            del self.stitches[stitch_id]
            self._save_stitches()
            return True
        return False

    def _save_stitches(self):
        """Save stitches to file."""
        # Get user's home directory
        home_dir = Path.home()
        stitches_dir = home_dir / ".aigency_extract" / "stitches"
        
        # Create directory if it doesn't exist
        stitches_dir.mkdir(parents=True, exist_ok=True)
        
        # Save stitches
        stitches_data = [stitch.model_dump() for stitch in self.stitches.values()]
        
        stitches_file = stitches_dir / "stitches.json"
        with open(stitches_file, "w") as f:
            json.dump(stitches_data, f, indent=2)


class StitchExecutor:
    """Execute stitches."""

    def __init__(
        self,
        provider_name: Optional[str] = None,
        model_name: Optional[str] = None,
        human_interaction_callback=None,
    ):
        """Initialize the stitch executor."""
        self.extractor = ContentExtractor(provider_name, model_name)
        self.human_interaction_callback = human_interaction_callback
        self.registry = StitchRegistry()

    def execute_stitch(
        self,
        stitch: Union[Stitch, str, int],
        content: Union[YouTubeContent, ArticleContent],
    ) -> Union[YouTubeContent, ArticleContent]:
        """Execute a stitch on content."""
        # Get the stitch if name or ID provided
        if isinstance(stitch, str):
            stitch_obj = self.registry.get_stitch_by_name(stitch)
            if not stitch_obj:
                # Try to create a simple stitch from comma-separated pattern names
                patterns = [p.strip() for p in stitch.split(",")]
                if patterns:
                    stitch_obj = Stitch(
                        name=f"Temporary stitch: {stitch}",
                        steps=[StitchStep(pattern_name=p) for p in patterns],
                    )
        elif isinstance(stitch, int):
            stitch_obj = self.registry.get_stitch(stitch)
        else:
            stitch_obj = stitch
        
        if not stitch_obj:
            raise ValueError(f"Stitch not found: {stitch}")
        
        # Execute each step
        result_content = content
        for i, step in enumerate(stitch_obj.steps):
            # Check if human interaction is required
            if step.human_in_loop and self.human_interaction_callback:
                # Call the human interaction callback
                should_continue, modified_content = self.human_interaction_callback(
                    step, result_content
                )
                if not should_continue:
                    break
                result_content = modified_content
            
            # Execute the pattern
            result_content = self.extractor.extract_content(
                result_content, step.pattern_name
            )
            
            # Update stitch information
            result_content.stitch_id = stitch_obj.id
            result_content.stitch_step = i + 1
        
        return result_content


# Singleton instance
stitch_registry = StitchRegistry()


def get_stitch(stitch_id: int) -> Optional[Stitch]:
    """Get a stitch by ID."""
    return stitch_registry.get_stitch(stitch_id)


def get_stitch_by_name(name: str) -> Optional[Stitch]:
    """Get a stitch by name."""
    return stitch_registry.get_stitch_by_name(name)


def get_all_stitches() -> List[Stitch]:
    """Get all stitches."""
    return stitch_registry.get_all_stitches()


def add_stitch(stitch: Stitch) -> int:
    """Add a new stitch."""
    return stitch_registry.add_stitch(stitch)


def remove_stitch(stitch_id: int) -> bool:
    """Remove a stitch."""
    return stitch_registry.remove_stitch(stitch_id)
