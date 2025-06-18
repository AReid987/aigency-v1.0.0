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

def test_tui_app():
    """Test the TUI application by running it briefly."""
    logger.info("Testing TUI application...")
    
    try:
        # Add the src directory to Python path
        src_dir = os.path.join(SCRIPT_DIR, "src")
        env = os.environ.copy()
        if "PYTHONPATH" in env:
            env["PYTHONPATH"] = f"{src_dir}:{env['PYTHONPATH']}"
        else:
            env["PYTHONPATH"] = src_dir
            
        logger.info(f"Using PYTHONPATH: {env.get('PYTHONPATH')}")
        
        # Start the TUI app process using the tui_main.py file
        tui_main_path = os.path.join(src_dir, "aigency_extract", "tui_main.py")
        logger.info(f"Running TUI app from: {tui_main_path}")
        
        process = subprocess.Popen(
            ["python", tui_main_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=SCRIPT_DIR,  # Run from the script directory
            env=env  # Use the modified environment
        )
        
        # Wait a few seconds to see if it crashes
        logger.info("Waiting for 5 seconds to check for immediate crashes...")
        time.sleep(5)
        
        # Check if the process is still running
        if process.poll() is None:
            logger.info("TUI app is running successfully!")
            # Terminate the process
            process.terminate()
            process.wait(timeout=5)
            return True
        else:
            # Process has exited
            stdout, stderr = process.communicate()
            logger.error(f"TUI app crashed with exit code {process.returncode}")
            logger.error(f"Stdout: {stdout}")
            logger.error(f"Stderr: {stderr}")
            return False
    except Exception as e:
        logger.error(f"Error testing TUI app: {e}")
        return False

def main():
    """Main function."""
    logger.info("Starting test script")
    logger.info(f"Script directory: {SCRIPT_DIR}")
    
    # Run the fix script
    if not run_fix_script():
        logger.error("Fix script failed, aborting test")
        return 1
    
    # Test the TUI app
    if test_tui_app():
        logger.info("Test completed successfully - TUI app is working!")
    else:
        logger.error("Test failed - TUI app is still not working")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
