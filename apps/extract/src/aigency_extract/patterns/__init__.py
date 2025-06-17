"""Pattern-based extraction functionality."""

from aigency_extract.patterns.extraction import ContentExtractor
from aigency_extract.patterns.registry import (add_pattern, get_all_patterns,
                                             get_pattern, get_pattern_names,
                                             remove_pattern)
from aigency_extract.patterns.stitches import (StitchExecutor, add_stitch,
                                             get_all_stitches, get_stitch,
                                             get_stitch_by_name,
                                             remove_stitch)

__all__ = [
    "ContentExtractor",
    "get_pattern",
    "get_all_patterns",
    "get_pattern_names",
    "add_pattern",
    "remove_pattern",
    "StitchExecutor",
    "get_stitch",
    "get_stitch_by_name",
    "get_all_stitches",
    "add_stitch",
    "remove_stitch",
]
