#!/usr/bin/env python
"""Simple fix script for the TUI application."""

import os
import sys
import shutil
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

def fix_tui_app():
    """Fix the TUI application."""
    # Path to the original file
    tui_path = Path("src/aigency_extract/app/tui.py")
    
    # Create a backup
    backup_path = Path("src/aigency_extract/app/tui.py.bak")
    shutil.copy2(tui_path, backup_path)
    print(f"Created backup at {backup_path}")
    
    # Create the fixed file content
    fixed_content = """\"\"\"Text User Interface for AIgency Extract.\"\"\"

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from dotenv import load_dotenv
from rich.text import Text
from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import (Button, DataTable, Footer, Header, Input, Label,
                            MarkdownViewer, Select, Static, TabPane, Tabs)

from aigency_extract.data.database import ExtractDatabase
from aigency_extract.data.models import (ContentType, LLMProvider, Stitch,
                                        StitchStep)
from aigency_extract.llm import get_llm
from aigency_extract.patterns import (ContentExtractor, StitchExecutor,
                                     add_stitch, get_pattern_names)
from aigency_extract.utils.article import create_article_content_shell
from aigency_extract.utils.youtube import create_youtube_content_shell, extract_video_id

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("aigency_extract_tui.log"),
        logging.StreamHandler()
    ]
)

# Load environment variables
load_dotenv()


class ExtractApp(App):
    \"\"\"Main TUI application for AIgency Extract.\"\"\"
    
    CSS = \"\"\"
    #sidebar {
        width: 25%;
        min-width: 20;
        border-right: solid $primary;
    }
    
    #main-content {
        width: 75%;
    }
    
    .content-list {
        height: 100%;
        overflow-y: auto;
    }
    
    .content-details {
        height: 100%;
        overflow-y: auto;
    }
    
    .search-container {
        height: auto;
        margin: 1 0;
    }
    
    .button-container {
        height: auto;
        align: center middle;
    }
    
    .extraction-form {
        height: auto;
        margin: 1 0;
    }
    
    .form-row {
        height: auto;
        margin: 1 0;
    }
    
    .form-label {
        width: 30%;
        content-align: right middle;
        padding-right: 1;
    }
    
    .form-input {
        width: 70%;
    }
    
    .status-message {
        text-align: center;
        background: $boost;
        color: $text;
        padding: 1;
    }
    
    .error-message {
        text-align: center;
        background: $error;
        color: $text;
        padding: 1;
    }
    
    .success-message {
        text-align: center;
        background: $success;
        color: $text;
        padding: 1;
    }
    
    .tag {
        background: $accent;
        color: $text;
        padding: 0 1;
        margin-right: 1;
    }
    
    .stitch-step {
        background: $surface;
        padding: 1;
        margin: 1 0;
        border: solid $primary;
    }
    \"\"\"
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("n", "new_extract", "New Extract"),
        ("r", "refresh", "Refresh"),
        ("f", "focus_search", "Search"),
        ("s", "new_stitch", "New Stitch"),
    ]
    
    def __init__(self):
        \"\"\"Initialize the application.\"\"\"
        super().__init__()
        self.logger = logging.getLogger("ExtractApp")
        self.logger.info("Initializing ExtractApp")
        self.db = ExtractDatabase()
        self.current_content_id = None
        
        # Get available LLM providers
        self.available_providers = []
        for provider in LLMProvider:
            env_var = f"{provider.value.upper()}_API_KEY"
            if os.environ.get(env_var):
                self.available_providers.append(provider.value)
        
        # Default provider
        self.default_provider = os.environ.get("DEFAULT_LLM_PROVIDER")
        if not self.default_provider and self.available_providers:
            self.default_provider = self.available_providers[0]
        
        self.logger.info(f"Available providers: {self.available_providers}")
        self.logger.info(f"Default provider: {self.default_provider}")
    
    def compose(self) -> ComposeResult:
        \"\"\"Compose the UI layout.\"\"\"
        yield Header()
        
        with Horizontal():
            # Sidebar
            with Vertical(id="sidebar"):
                with Container(classes="search-container"):
                    yield Input(placeholder="Search extracts...", id="search-input")
                    with Horizontal(classes="button-container"):
                        yield Button("Search", id="search-button", variant="primary")
                        yield Button("New", id="new-button", variant="success")
                
                # Content list
                yield Static("Extracts", classes="heading")
                yield DataTable(id="content-table", classes="content-list")
            
            # Main content area
            with Vertical(id="main-content"):
                with Tabs() as tabs:
                    # Details tab
                    with TabPane("Details", id="details-tab"):
                        yield MarkdownViewer(id="content-details", classes="content-details")
                    
                    # Extract tab
                    with TabPane("Extract", id="extract-tab"):
                        with Container(classes="extraction-form"):
                            with Horizontal(classes="form-row"):
                                yield Label("URL:", classes="form-label")
                                yield Input(placeholder="YouTube URL or article URL", id="url-input", classes="form-input")
                            
                            with Horizontal(classes="form-row"):
                                yield Label("Type:", classes="form-label")
                                yield Select(
                                    [(label, value) for value, label in [
                                        ("youtube", "YouTube Video"),
                                        ("article", "Article"),
                                    ]],
                                    id="content-type-select",
                                    value="youtube",
                                    classes="form-input"
                                )
                            
                            with Horizontal(classes="form-row"):
                                yield Label("Pattern:", classes="form-label")
                                yield Select(
                                    [(pattern, pattern) for pattern in get_pattern_names()],
                                    id="pattern-select",
                                    value="youtube_summary" if "youtube_summary" in get_pattern_names() else get_pattern_names()[0] if get_pattern_names() else "",
                                    classes="form-input"
                                )
                            
                            with Horizontal(classes="form-row"):
                                yield Label("Provider:", classes="form-label")
                                yield Select(
                                    [(provider, provider) for provider in self.available_providers],
                                    id="provider-select",
                                    value=self.default_provider,
                                    classes="form-input"
                                )
                            
                            with Horizontal(classes="button-container"):
                                yield Button("Extract", id="extract-button", variant="primary")
                            
                            yield Static("", id="extract-status", classes="status-message")
                    
                    # Stitch tab
                    with TabPane("Stitch", id="stitch-tab"):
                        with Container(classes="extraction-form"):
                            with Horizontal(classes="form-row"):
                                yield Label("URL:", classes="form-label")
                                yield Input(placeholder="YouTube URL or article URL", id="stitch-url-input", classes="form-input")
                            
                            with Horizontal(classes="form-row"):
                                yield Label("Stitch:", classes="form-label")
                                yield Select(
                                    self._get_stitch_options(),
                                    id="stitch-select",
                                    classes="form-input"
                                )
                            
                            with Horizontal(classes="form-row"):
                                yield Label("Provider:", classes="form-label")
                                yield Select(
                                    [(provider, provider) for provider in self.available_providers],
                                    id="stitch-provider-select",
                                    value=self.default_provider,
                                    classes="form-input"
                                )
                            
                            with Horizontal(classes="button-container"):
                                yield Button("Run Stitch", id="run-stitch-button", variant="primary")
                                yield Button("Create New", id="create-stitch-button", variant="success")
                            
                            yield Static("", id="stitch-status", classes="status-message")
                    
                    # Settings tab
                    with TabPane("Settings", id="settings-tab"):
                        with Container(classes="extraction-form"):
                            with Horizontal(classes="form-row"):
                                yield Label("Default Provider:", classes="form-label")
                                yield Select(
                                    [(provider, provider) for provider in self.available_providers],
                                    id="default-provider-select",
                                    value=self.default_provider,
                                    classes="form-input"
                                )
                            
                            with Horizontal(classes="form-row"):
                                yield Label("Database Path:", classes="form-label")
                                yield Input(
                                    value=self.db.db_path,
                                    id="db-path-input",
                                    disabled=True,
                                    classes="form-input"
                                )
                            
                            with Horizontal(classes="button-container"):
                                yield Button("Save Settings", id="save-settings-button", variant="primary")
                            
                            yield Static("", id="settings-status", classes="status-message")
        
        yield Footer()
    
    def on_mount(self) -> None:
        \"\"\"Set up the UI when the app is mounted.\"\"\"
        self.logger.info("Mounting app")
        
        # Set up content table
        table = self.query_one("#content-table", DataTable)
        table.add_columns("ID", "Title", "Type", "Date", "Pattern")
        
        # Load initial data
        self.refresh_content_list()
        
        # Log that the app is mounted
        self.logger.info("App mounted successfully")
"""
    
    # Write the rest of the file content
    with open("rest_of_file.txt", "r") as f:
        fixed_content += f.read()
    
    # Write the fixed content to the file
    with open(tui_path, "w") as f:
        f.write(fixed_content)
    
    print(f"Fixed {tui_path}")
    print("Run the application with: python run_tui.py")

if __name__ == "__main__":
    fix_tui_app()
