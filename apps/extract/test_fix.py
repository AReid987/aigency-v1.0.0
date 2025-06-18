#!/usr/bin/env python
"""Test script to verify the TUI application fix."""

import os
import sys
import logging
import subprocess
import time
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("test_fix.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("test_fix")

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()

def run_fix_script():
    """Run the fix script."""
    logger.info("Running fix script...")
    
    try:
        fix_script_path = os.path.join(SCRIPT_DIR, "fix_tui.py")
        result = subprocess.run(
            ["python", fix_script_path],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info(f"Fix script output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Fix script failed: {e}")
        logger.error(f"Error output: {e.stderr}")
        return False

def verify_fix():
    """Verify that the fix was applied correctly by checking the file content."""
    logger.info("Verifying fix...")
    
    # Path to the TUI file
    tui_path = os.path.join(SCRIPT_DIR, "src/aigency_extract/app/tui.py")
    
    # Check if the file exists
    if not os.path.exists(tui_path):
        logger.error(f"TUI file not found at {tui_path}")
        return False
    
    # Read the file
    with open(tui_path, "r") as f:
        content = f.read()
    
    # Check if the DataTable columns are set up in the compose method
    if "yield DataTable(id=\"content-table\"" in content and "table.add_columns" in content:
        logger.info("DataTable columns are set up in the compose method")
        
        # Check if the on_mount method is simplified
        on_mount_start = content.find("def on_mount(self)")
        if on_mount_start != -1:
            on_mount_content = content[on_mount_start:content.find("def ", on_mount_start + 1)]
            if "table.add_columns" not in on_mount_content:
                logger.info("on_mount method is simplified (no table.add_columns)")
                return True
    
    logger.error("Fix was not applied correctly")
    return False

def main():
    """Main function."""
    logger.info("Starting test script")
    logger.info(f"Script directory: {SCRIPT_DIR}")
    
    # Run the fix script
    if not run_fix_script():
        logger.error("Fix script failed, aborting test")
        return 1
    
    # Verify the fix
    if verify_fix():
        logger.info("Fix verification successful!")
        return 0
    else:
        logger.error("Fix verification failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
