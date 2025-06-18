#!/usr/bin/env python
"""Fix indentation issues in the TUI file."""

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
        logging.FileHandler("fix_indentation.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("fix_indentation")

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()

def backup_file(file_path):
    """Create a backup of the file."""
    backup_path = f"{file_path}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
    shutil.copy2(file_path, backup_path)
    logger.info(f"Created backup at {backup_path}")
    return backup_path

def fix_indentation():
    """Fix indentation issues in the TUI file."""
    # Path to the TUI file
    tui_path = os.path.join(SCRIPT_DIR, "src/aigency_extract/app/tui.py")
    
    # Check if the file exists
    if not os.path.exists(tui_path):
        logger.error(f"TUI file not found at {tui_path}")
        return False
    
    logger.info(f"Using TUI file at: {tui_path}")
    
    # Create a backup
    backup_path = backup_file(tui_path)
    
    # Read the file line by line
    with open(tui_path, "r") as f:
        lines = f.readlines()
    
    # Fix indentation issues
    fixed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for the problematic line
        if line.strip() == "def action_new_extract(self) -> None:":
            # This should be at the correct indentation level (4 spaces)
            fixed_lines.append("    def action_new_extract(self) -> None:\n")
            i += 1
            
            # Skip the docstring line and add it with correct indentation
            if i < len(lines) and '"""Focus the extract tab."""' in lines[i]:
                fixed_lines.append("        \"\"\"Focus the extract tab.\"\"\"\n")
                i += 1
            else:
                # If the docstring is missing, add it
                fixed_lines.append("        \"\"\"Focus the extract tab.\"\"\"\n")
        
        # Check for other problematic methods
        elif line.strip() == "def action_new_stitch(self) -> None:":
            # This should be at the correct indentation level (4 spaces)
            fixed_lines.append("    def action_new_stitch(self) -> None:\n")
            i += 1
            
            # Skip the docstring line and add it with correct indentation
            if i < len(lines) and '"""Focus the stitch tab."""' in lines[i]:
                fixed_lines.append("        \"\"\"Focus the stitch tab.\"\"\"\n")
                i += 1
            else:
                # If the docstring is missing, add it
                fixed_lines.append("        \"\"\"Focus the stitch tab.\"\"\"\n")
        
        # Check for other problematic methods
        elif line.strip() == "def new_extract(self) -> None:":
            # This should be at the correct indentation level (4 spaces)
            fixed_lines.append("    def new_extract(self) -> None:\n")
            i += 1
            
            # Skip the docstring line and add it with correct indentation
            if i < len(lines) and '"""Create a new extract."""' in lines[i]:
                fixed_lines.append("        \"\"\"Create a new extract.\"\"\"\n")
                i += 1
            else:
                # If the docstring is missing, add it
                fixed_lines.append("        \"\"\"Create a new extract.\"\"\"\n")
        
        else:
            fixed_lines.append(line)
            i += 1
    
    # Write the fixed content back to the file
    with open(tui_path, "w") as f:
        f.writelines(fixed_lines)
    
    logger.info(f"Successfully fixed indentation in {tui_path}")
    logger.info(f"Backup saved at {backup_path}")
    
    return True

def main():
    """Main function."""
    logger.info("Starting indentation fix script")
    logger.info(f"Script directory: {SCRIPT_DIR}")
    
    # Fix indentation issues
    if fix_indentation():
        logger.info("Fix completed successfully")
    else:
        logger.error("Fix failed")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
