#!/usr/bin/env python
"""Test script for the fixed TUI application."""

import asyncio
import os
import sys
import time
from contextlib import contextmanager

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from textual.driver import Driver
from textual.events import Key

from aigency_extract.app.tui import ExtractApp

@contextmanager
def redirect_stderr_to_file(file_path):
    """Redirect stderr to a file."""
    import sys
    original_stderr = sys.stderr
    with open(file_path, 'w') as file:
        sys.stderr = file
        try:
            yield
        finally:
            sys.stderr = original_stderr

async def test_tab_switching():
    """Test switching between tabs and focusing inputs."""
    # Create a driver for the app
    app = ExtractApp()
    driver = Driver(app)
    
    # Start the app
    async with driver.run_test():
        # Wait for the app to initialize
        await asyncio.sleep(2)
        
        # Test switching to extract tab
        print("Switching to extract tab...")
        await app.press("n")
        await asyncio.sleep(2)
        
        # Try to find the URL input in the extract tab
        try:
            url_input = app.query_one("#url-input")
            print(f"Found URL input: {url_input}")
        except Exception as e:
            print(f"Error finding URL input: {e}")
        
        # Test switching to stitch tab
        print("Switching to stitch tab...")
        await app.press("s")
        await asyncio.sleep(2)
        
        # Try to find the URL input in the stitch tab
        try:
            stitch_url_input = app.query_one("#stitch-url-input")
            print(f"Found stitch URL input: {stitch_url_input}")
        except Exception as e:
            print(f"Error finding stitch URL input: {e}")
        
        # Test pressing 'q' key to quit
        print("Quitting app...")
        await app.press("q")
        await asyncio.sleep(1)
    
    print("Test completed successfully!")

if __name__ == "__main__":
    # First, run the fix script
    print("Running fix script...")
    import fix_tui
    fix_tui.fix_tui_app()
    
    # Then run the test
    print("Running test...")
    with redirect_stderr_to_file("fixed_tui_test.log"):
        asyncio.run(test_tab_switching())
