#!/usr/bin/env python
"""Test script for the TUI fix."""

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

async def test_key_bindings():
    """Test the key bindings for the TUI app."""
    # Create a driver for the app
    app = ExtractApp()
    driver = Driver(app)
    
    # Start the app
    async with driver.run_test():
        # Wait for the app to initialize
        await asyncio.sleep(1)
        
        # Test pressing 'n' key
        print("Testing 'n' key...")
        await app.press("n")
        await asyncio.sleep(1)
        
        # Test pressing 's' key
        print("Testing 's' key...")
        await app.press("s")
        await asyncio.sleep(1)
        
        # Test pressing 'q' key to quit
        print("Testing 'q' key...")
        await app.press("q")
        await asyncio.sleep(1)
    
    print("Test completed successfully!")

if __name__ == "__main__":
    # Redirect stderr to a file to capture any errors
    with redirect_stderr_to_file("tui_test_errors.log"):
        asyncio.run(test_key_bindings())
