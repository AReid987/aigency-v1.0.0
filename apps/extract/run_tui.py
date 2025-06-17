#!/usr/bin/env python
"""Run the AIgency Extract TUI."""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from aigency_extract.app.tui import run_tui

if __name__ == "__main__":
    run_tui()
