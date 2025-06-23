#!/usr/bin/env python
"""Fix script for the TUI application's tab IDs."""

import os
import sys
import logging
import shutil
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fix_tab_ids")

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()

def fix_tab_ids():
    """Fix the tab IDs in the TUI application."""
    # Path to the TUI file
    tui_path = os.path.join(SCRIPT_DIR, "src/aigency_extract/app/tui.py")
    
    # Check if the file exists
    if not os.path.exists(tui_path):
        logger.error(f"TUI file not found at {tui_path}")
        return False
    
    logger.info(f"Using TUI file at: {tui_path}")
    
    # Create a backup
    backup_path = f"{tui_path}.bak"
    shutil.copy2(tui_path, backup_path)
    logger.info(f"Created backup at {backup_path}")
    
    # Read the file
    with open(tui_path, "r") as f:
        content = f.read()
    
    # Replace the Tabs section with a fixed version
    old_tabs_line = "with Tabs() as tabs:"
    new_tabs_line = "with Tabs(id=\"main-tabs\") as tabs:"
    content = content.replace(old_tabs_line, new_tabs_line)
    logger.info("Fixed Tabs initialization")
    
    # Write the updated content back to the file
    with open(tui_path, "w") as f:
        f.write(content)
    
    logger.info(f"Successfully updated {tui_path}")
    
    return True

if __name__ == "__main__":
    logger.info("Starting fix script")
    
    # Fix the tab IDs
    if fix_tab_ids():
        logger.info("Fix completed successfully")
        sys.exit(0)
    else:
        logger.error("Fix failed")
        sys.exit(1)
