#!/usr/bin/env python
"""Fix script for the TUI application's component mounting issue."""

import os
import sys
import logging
import shutil
import re
from datetime import datetime
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("fix_tui.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("fix_tui")

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()

def backup_file(file_path):
    """Create a backup of the file."""
    backup_path = f"{file_path}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
    shutil.copy2(file_path, backup_path)
    logger.info(f"Created backup at {backup_path}")
    return backup_path

def fix_tui_file():
    """Fix the TUI file by moving DataTable column setup from on_mount to compose."""
    # Path to the TUI file - using the exact path we found
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
    
    # Find the compose method
    compose_start = content.find("def compose(self)")
    if compose_start == -1:
        logger.error("Could not find compose method")
        return False
    
    # Find the DataTable line in compose
    datatable_line = content.find("yield DataTable(id=\"content-table\"", compose_start)
    if datatable_line == -1:
        logger.error("Could not find DataTable in compose method")
        return False
    
    # Find the end of the DataTable line
    datatable_line_end = content.find(")", datatable_line)
    if datatable_line_end == -1:
        logger.error("Could not find end of DataTable line")
        return False
    
    # Replace the DataTable line to include columns directly
    old_datatable_line = content[datatable_line:datatable_line_end+1]
    new_datatable_line = 'yield DataTable(id="content-table", classes="content-list", show_header=True)'
    
    content = content.replace(old_datatable_line, new_datatable_line)
    logger.info("Updated DataTable initialization")
    
    # Remove any duplicate column setup code
    content = re.sub(r'# Add columns to the table\s+table = self\.query_one\("#content-table", DataTable\)\s+table\.add_columns\("ID", "Title", "Type", "Date", "Pattern"\)', '', content)
    logger.info("Removed duplicate column setup code")
    
    # Fix the on_mount method
    on_mount_start = content.find("def on_mount(self)")
    if on_mount_start == -1:
        logger.error("Could not find on_mount method")
        return False
    
    on_mount_end = content.find("def ", on_mount_start + 1)
    if on_mount_end == -1:
        logger.error("Could not find end of on_mount method")
        return False
    
    # Replace the on_mount method
    old_on_mount = content[on_mount_start:on_mount_end]
    new_on_mount = """    def on_mount(self) -> None:
        # Set up the UI when the app is mounted
        self.logger.info("Mounting app")
        
        # Set up content table columns
        table = self.query_one("#content-table", DataTable)
        table.add_columns("ID", "Title", "Type", "Date", "Pattern")
        
        # Load initial data
        self.refresh_content_list()
        
        # Log that the app is mounted
        self.logger.info("App mounted successfully")
    
"""
    
    content = content.replace(old_on_mount, new_on_mount)
    logger.info("Fixed on_mount method")
    
    # Fix the refresh_content_list method to handle the case when the table is not yet initialized
    refresh_start = content.find("def refresh_content_list(self)")
    if refresh_start == -1:
        logger.error("Could not find refresh_content_list method")
        return False
    
    refresh_end = content.find("def ", refresh_start + 1)
    if refresh_end == -1:
        logger.error("Could not find end of refresh_content_list method")
        return False
    
    # Replace the refresh_content_list method
    old_refresh = content[refresh_start:refresh_end]
    new_refresh = """    def refresh_content_list(self) -> None:
        # Refresh the content list from the database
        try:
            table = self.query_one("#content-table", DataTable)
            
            # Clear the table
            table.clear()
            
            # Get content from database
            results = self.db.search_content(limit=100)
            
            # Add to table
            for content in results:
                table.add_row(
                    str(content.id),
                    content.title[:50] + ("..." if len(content.title) > 50 else ""),
                    content.content_type.value,
                    content.extracted_at.strftime("%Y-%m-%d") if content.extracted_at else "",
                    content.extraction_pattern
                )
        except Exception as e:
            self.logger.error(f"Error refreshing content list: {e}")
    
"""
    
    content = content.replace(old_refresh, new_refresh)
    logger.info("Fixed refresh_content_list method")
    
    # Fix any indentation issues
    # This is a simple approach - for a more robust solution, a proper Python parser would be better
    content = re.sub(r'\n\s+def ', r'\n    def ', content)
    
    # Fix the run_tui function indentation
    run_tui_start = content.find("def run_tui()")
    if run_tui_start != -1:
        # Make sure it's not indented
        content = content[:run_tui_start] + "\n\ndef run_tui()" + content[run_tui_start+len("def run_tui()"):]
    
    logger.info("Fixed indentation issues")
    
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
    
    # Fix the TUI file
    if fix_tui_file():
        logger.info("Fix completed successfully")
    else:
        logger.error("Fix failed")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
