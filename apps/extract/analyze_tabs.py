#!/usr/bin/env python
"""Script to analyze the tab structure in the TUI application."""

import os
import sys
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("analyze_tabs.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("analyze_tabs")

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()

def analyze_tabs():
    """Analyze the tab structure in the TUI application."""
    # Path to the TUI file
    tui_path = os.path.join(SCRIPT_DIR, "src/aigency_extract/app/tui.py")
    
    # Check if the file exists
    if not os.path.exists(tui_path):
        logger.error(f"TUI file not found at {tui_path}")
        return False
    
    logger.info(f"Using TUI file at: {tui_path}")
    
    # Read the file
    with open(tui_path, "r") as f:
        content = f.read()
    
    # Find the Tabs section in the compose method
    compose_start = content.find("def compose(self)")
    if compose_start == -1:
        logger.error("Could not find compose method")
        return False
    
    tabs_section_start = content.find("with Tabs()", compose_start)
    if tabs_section_start == -1:
        logger.error("Could not find Tabs section in compose method")
        return False
    
    # Extract a portion of the Tabs section for analysis
    tabs_section = content[tabs_section_start:tabs_section_start + 500]
    logger.info(f"Tabs section excerpt:\n{tabs_section}")
    
    # Find all references to extract-tab and stitch-tab
    extract_tab_refs = []
    pos = 0
    while True:
        extract_tab_start = content.find("extract-tab", pos)
        if extract_tab_start == -1:
            break
        
        extract_tab_line_start = content.rfind("\n", 0, extract_tab_start) + 1
        extract_tab_line_end = content.find("\n", extract_tab_start)
        if extract_tab_line_end == -1:
            extract_tab_line_end = len(content)
        
        extract_tab_line = content[extract_tab_line_start:extract_tab_line_end]
        extract_tab_refs.append(extract_tab_line)
        pos = extract_tab_line_end + 1
    
    logger.info(f"Found {len(extract_tab_refs)} references to extract-tab:")
    for i, ref in enumerate(extract_tab_refs[:10]):  # Limit to first 10 for brevity
        logger.info(f"  {i+1}: {ref}")
    
    stitch_tab_refs = []
    pos = 0
    while True:
        stitch_tab_start = content.find("stitch-tab", pos)
        if stitch_tab_start == -1:
            break
        
        stitch_tab_line_start = content.rfind("\n", 0, stitch_tab_start) + 1
        stitch_tab_line_end = content.find("\n", stitch_tab_start)
        if stitch_tab_line_end == -1:
            stitch_tab_line_end = len(content)
        
        stitch_tab_line = content[stitch_tab_line_start:stitch_tab_line_end]
        stitch_tab_refs.append(stitch_tab_line)
        pos = stitch_tab_line_end + 1
    
    logger.info(f"Found {len(stitch_tab_refs)} references to stitch-tab:")
    for i, ref in enumerate(stitch_tab_refs[:10]):  # Limit to first 10 for brevity
        logger.info(f"  {i+1}: {ref}")
    
    return True

def main():
    """Main function."""
    logger.info("Starting analysis")
    logger.info(f"Script directory: {SCRIPT_DIR}")
    
    # Analyze the tab structure
    if analyze_tabs():
        logger.info("Analysis completed successfully")
    else:
        logger.error("Analysis failed")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
