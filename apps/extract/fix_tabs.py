#!/usr/bin/env python
"""Fix script for the TUI application's tab structure."""

import os
import sys
import logging
import shutil
from datetime import datetime
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("fix_tabs.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("fix_tabs")

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()

def backup_file(file_path):
    """Create a backup of the file."""
    backup_path = f"{file_path}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
    shutil.copy2(file_path, backup_path)
    logger.info(f"Created backup at {backup_path}")
    return backup_path

def fix_tab_structure():
    """Fix the tab structure in the TUI application."""
    # Path to the TUI file
    tui_path = os.path.join(SCRIPT_DIR, "src/aigency_extract/app/tui.py")
    
    # Check if the file exists
    if not os.path.exists(tui_path):
        logger.error(f"TUI file not found at {tui_path}")
        return False
    
    logger.info(f"Using TUI file at: {tui_path}")
    
    # Create a backup
    backup_path = backup_file(tui_path)
    
    # Read the file
    with open(tui_path, "r") as f:
        content = f.read()
    
    # Fix the action_new_extract method
    action_new_extract_start = content.find("def action_new_extract(self)")
    if action_new_extract_start != -1:
        action_new_extract_end = content.find("def ", action_new_extract_start + 1)
        if action_new_extract_end != -1:
            old_action_new_extract = content[action_new_extract_start:action_new_extract_end]
            new_action_new_extract = """    def action_new_extract(self) -> None:
        """Focus the extract tab."""
        self.logger.info("Action: new_extract")
        
        try:
            # First, check if the extract tab exists
            tabs = self.query_one(Tabs)
            tab_panes = list(tabs.query("TabPane"))
            extract_tab = None
            
            for tab in tab_panes:
                if tab.id == "extract-tab":
                    extract_tab = tab
                    break
            
            if not extract_tab:
                self.logger.error(f"Extract tab not found. Available tabs: {[tab.id for tab in tab_panes]}")
                self.notify("Error: Extract tab not found", severity="error")
                return
            
            # Switch to the extract tab
            tabs.active = "extract-tab"
            
            # Make sure the tab is fully rendered
            self.refresh()
            
            # Use a longer delay to ensure the tab is fully rendered
            self.set_timer(1.0, self._ensure_extract_tab_ready)
        except Exception as e:
            self.logger.error(f"Error in action_new_extract: {e}")
            self.notify(f"Error: {str(e)}", severity="error")

"""
            content = content.replace(old_action_new_extract, new_action_new_extract)
            logger.info("Fixed action_new_extract method")
    
    # Fix the action_new_stitch method
    action_new_stitch_start = content.find("def action_new_stitch(self)")
    if action_new_stitch_start != -1:
        action_new_stitch_end = content.find("def ", action_new_stitch_start + 1)
        if action_new_stitch_end != -1:
            old_action_new_stitch = content[action_new_stitch_start:action_new_stitch_end]
            new_action_new_stitch = """    def action_new_stitch(self) -> None:
        """Focus the stitch tab."""
        self.logger.info("Action: new_stitch")
        
        try:
            # First, check if the stitch tab exists
            tabs = self.query_one(Tabs)
            tab_panes = list(tabs.query("TabPane"))
            stitch_tab = None
            
            for tab in tab_panes:
                if tab.id == "stitch-tab":
                    stitch_tab = tab
                    break
            
            if not stitch_tab:
                self.logger.error(f"Stitch tab not found. Available tabs: {[tab.id for tab in tab_panes]}")
                self.notify("Error: Stitch tab not found", severity="error")
                return
            
            # Switch to the stitch tab
            tabs.active = "stitch-tab"
            
            # Make sure the tab is fully rendered
            self.refresh()
            
            # Use a longer delay to ensure the tab is fully rendered
            self.set_timer(1.0, self._ensure_stitch_tab_ready)
        except Exception as e:
            self.logger.error(f"Error in action_new_stitch: {e}")
            self.notify(f"Error: {str(e)}", severity="error")

"""
            content = content.replace(old_action_new_stitch, new_action_new_stitch)
            logger.info("Fixed action_new_stitch method")
    
    # Write the updated content back to the file
    with open(tui_path, "w") as f:
        f.write(content)
    
    logger.info(f"Successfully updated {tui_path}")
    logger.info(f"Backup saved at {backup_path}")
    
    return True

def main():
    """Main function."""
    logger.info("Starting fix script")
    logger.info(f"Script directory: {SCRIPT_DIR}")
    
    # Fix the tab structure
    if fix_tab_structure():
        logger.info("Fix completed successfully")
    else:
        logger.error("Fix failed")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
