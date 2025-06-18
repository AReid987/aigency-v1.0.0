#!/usr/bin/env python
"""Simple test script for the TUI application."""

import os
import sys
import logging

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("test_run.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("test_run")

def main():
    """Run the test."""
    logger.info("Starting test")
    
    try:
        # Import the ExtractApp class directly
        from aigency_extract.app.tui import ExtractApp
        
        # Create an instance of the app
        app = ExtractApp()
        
        # Run the app
        app.run()
        
    except Exception as e:
        logger.error(f"Error running test: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
