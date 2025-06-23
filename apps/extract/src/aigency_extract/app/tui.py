"""Text User Interface for AIgency Extract."""

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
    """Main TUI application for AIgency Extract."""
    
    CSS = """
    #sidebar {
        width: 25%;
        min-width: 20;
        border-right: solid $primary;
    }
    
    #main-content {
        width: 75%;
    }
    
    .content-list {
        height: 30%;
        border: solid $primary;
    }
    
    .content-details {
        height: 70%;
        border: solid $primary;
    }
    
    .extraction-form {
        padding: 1 2;
    }
    
    .form-row {
        height: auto;
        margin-bottom: 1;
    }
    
    .form-label {
        width: 20%;
        content-align: right middle;
        padding-right: 1;
    }
    
    .form-input {
        width: 80%;
    }
    
    .form-button {
        margin-right: 1;
    }
    
    .settings-section {
        margin-bottom: 2;
    }
    
    .settings-title {
        text-style: bold;
        margin-bottom: 1;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
        ("f", "search", "Search"),
        ("n", "new_extract", "New Extract"),
        ("s", "new_stitch", "New Stitch"),
        ("ctrl+p", "palette", "palette"),
    ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger("ExtractApp")
        self.logger.info("Initializing ExtractApp")
        
        # Initialize database
        self.db = ExtractDatabase()
        
        # Initialize LLM providers
        self.providers = ['gemini', 'mistral', 'groq', 'huggingface', 'openrouter', 'voidai', 'cerebras', 'chutes']
        self.logger.info(f"Available providers: {self.providers}")
        
        # Set default provider
        self.default_provider = os.getenv("DEFAULT_LLM_PROVIDER", "mistral")
        self.logger.info(f"Default provider: {self.default_provider}")
        
        # Track current content
        self.current_content_id = None
        
        # Track retry counts for focus attempts
        self.extract_focus_retry_count = 0
        self.stitch_focus_retry_count = 0
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        # Create header and footer
        yield Header()
        yield Footer()
        
        # Create main layout
        with Horizontal():
            # Sidebar with content list
            with Vertical(id="sidebar"):
                yield DataTable(id="content-table", classes="content-list", show_header=True)
            
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
                                yield Input(placeholder="Enter YouTube URL or article URL", id="extract-url", classes="form-input")
                            
                            with Horizontal(classes="form-row"):
                                yield Label("Type:", classes="form-label")
                                yield Select(
                                    [(ct.value, ct.value) for ct in ContentType],
                                    id="content-type",
                                    value=ContentType.YOUTUBE.value,
                                    classes="form-input"
                                )
                            
                            with Horizontal(classes="form-row"):
                                yield Label("Pattern:", classes="form-label")
                                yield Select(
                                    [(p, p) for p in get_pattern_names()],
                                    id="extraction-pattern",
                                    classes="form-input"
                                )
                            
                            with Horizontal(classes="form-row"):
                                yield Label("Provider:", classes="form-label")
                                yield Select(
                                    [(p, p) for p in self.providers],
                                    id="llm-provider",
                                    value=self.default_provider,
                                    classes="form-input"
                                )
                            
                            with Horizontal(classes="form-row"):
                                yield Button("Extract", id="extract-button", variant="primary", classes="form-button")
                                yield Button("Clear", id="extract-clear-button", variant="default", classes="form-button")
                    
                    # Stitch tab
                    with TabPane("Stitch", id="stitch-tab"):
                        with Container(classes="extraction-form"):
                            with Horizontal(classes="form-row"):
                                yield Label("Name:", classes="form-label")
                                yield Input(placeholder="Enter stitch name", id="stitch-name", classes="form-input")
                            
                            with Horizontal(classes="form-row"):
                                yield Label("Description:", classes="form-label")
                                yield Input(placeholder="Enter stitch description", id="stitch-description", classes="form-input")
                            
                            with Horizontal(classes="form-row"):
                                yield Label("Provider:", classes="form-label")
                                yield Select(
                                    [(p, p) for p in self.providers],
                                    id="stitch-provider",
                                    value=self.default_provider,
                                    classes="form-input"
                                )
                            
                            with Horizontal(classes="form-row"):
                                yield Button("Create", id="stitch-create-button", variant="primary", classes="form-button")
                                yield Button("Clear", id="stitch-clear-button", variant="default", classes="form-button")
                    
                    # Settings tab
                    with TabPane("Settings", id="settings-tab"):
                        with Container(classes="extraction-form"):
                            with Horizontal(classes="form-row"):
                                yield Label("Default Provider:", classes="form-label")
                                yield Select(
                                    [(p, p) for p in self.providers],
                                    id="default-provider",
                                    value=self.default_provider,
                                    classes="form-input"
                                )
                            
                            with Horizontal(classes="form-row"):
                                yield Button("Save", id="settings-save-button", variant="primary", classes="form-button")
                                yield Button("Reset", id="settings-reset-button", variant="default", classes="form-button")
    
    def on_mount(self) -> None:
        """Set up the UI when the app is mounted."""
        self.logger.info("Mounting app")
        
        # Set up content table columns
        table = self.query_one("#content-table", DataTable)
        table.add_columns("ID", "Title", "Type", "Date", "Pattern")
        
        # Load initial data
        self.refresh_content_list()
        
        # Log that the app is mounted
        self.logger.info("App mounted successfully")
    
    def refresh_content_list(self) -> None:
        """Refresh the content list from the database."""
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
    
    def action_refresh(self) -> None:
        """Refresh the content list."""
        self.refresh_content_list()
    
    def action_new_extract(self) -> None:
        """Focus the extract tab."""
        self.logger.info("Action: new_extract")
        
        try:
            # First, check if the extract tab exists
            tabs = self.query_one(Tabs)
            tab_ids = [tab.id for tab in tabs.query("TabPane")]
            
            if "extract-tab" not in tab_ids:
                self.logger.error(f"Extract tab not found. Available tabs: {tab_ids}")
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
    
    def _ensure_extract_tab_ready(self) -> None:
        """Ensure the extract tab is ready and then focus the URL input."""
        # Check if we're on the extract tab
        tabs = self.query_one(Tabs)
        if tabs.active != "extract-tab":
            self.logger.error("Extract tab is not active, cannot proceed")
            return
        
        # Try to focus the URL input
        self._focus_extract_url_input()
    
    def _focus_extract_url_input(self, retry_count=0) -> None:
        """Focus the URL input in the extract tab."""
        max_retries = 5
        
        try:
            # Check if the tab is active before trying to focus
            tabs = self.query_one(Tabs)
            if tabs.active != "extract-tab":
                self.logger.error("Extract tab is not active, cannot focus input")
                # Try again with incremented retry count after a longer delay
                if retry_count < max_retries:
                    self.set_timer(0.5, lambda: self._focus_extract_url_input(retry_count + 1))
                return
            
            # Try to find the input directly
            try:
                url_input = self.query_one("#extract-url", Input)
                url_input.focus()
                self.logger.info("Focused extract URL input")
                return
            except Exception as e:
                self.logger.error(f"Could not find extract URL input: {e}")
                
            # Fallback: try to find the extract tab and then search within it
            extract_tab = self.query_one("#extract-tab", TabPane)
            
            # Check if the tab has been populated with content
            url_input = extract_tab.query_one("#extract-url", Input)
            url_input.focus()
            self.logger.info("Focused extract URL input (via tab)")
        except Exception as e:
            self.logger.error(f"Error focusing extract URL input: {e}")
            
            # Try again with incremented retry count after a longer delay
            if retry_count < max_retries:
                self.set_timer(0.5, lambda: self._focus_extract_url_input(retry_count + 1))
    
    def action_new_stitch(self) -> None:
        """Focus the stitch tab."""
        self.logger.info("Action: new_stitch")
        
        try:
            # First, check if the stitch tab exists
            tabs = self.query_one(Tabs)
            tab_ids = [tab.id for tab in tabs.query("TabPane")]
            
            if "stitch-tab" not in tab_ids:
                self.logger.error(f"Stitch tab not found. Available tabs: {tab_ids}")
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
    
    def _ensure_stitch_tab_ready(self) -> None:
        """Ensure the stitch tab is ready and then focus the name input."""
        # Check if we're on the stitch tab
        tabs = self.query_one(Tabs)
        if tabs.active != "stitch-tab":
            self.logger.error("Stitch tab is not active, cannot proceed")
            return
        
        # Try to focus the name input
        self._focus_stitch_name_input()
    
    def _focus_stitch_name_input(self, retry_count=0) -> None:
        """Focus the name input in the stitch tab."""
        max_retries = 5
        
        try:
            # Check if the tab is active before trying to focus
            tabs = self.query_one(Tabs)
            if tabs.active != "stitch-tab":
                self.logger.error("Stitch tab is not active, cannot focus input")
                # Try again with incremented retry count after a longer delay
                if retry_count < max_retries:
                    self.set_timer(0.5, lambda: self._focus_stitch_name_input(retry_count + 1))
                return
            
            # Try to find the input directly
            try:
                name_input = self.query_one("#stitch-name", Input)
                name_input.focus()
                self.logger.info("Focused stitch name input")
                return
            except Exception as e:
                self.logger.error(f"Could not find stitch name input: {e}")
                
            # Fallback: try to find the stitch tab and then search within it
            stitch_tab = self.query_one("#stitch-tab", TabPane)
            
            # Check if the tab has been populated with content
            name_input = stitch_tab.query_one("#stitch-name", Input)
            name_input.focus()
            self.logger.info("Focused stitch name input (via tab)")
        except Exception as e:
            self.logger.error(f"Error focusing stitch name input: {e}")
            
            # Try again with incremented retry count after a longer delay
            if retry_count < max_retries:
                self.set_timer(0.5, lambda: self._focus_stitch_name_input(retry_count + 1))
    
    def action_search(self) -> None:
        """Show search dialog."""
        self.logger.info("Action: search")
        # TODO: Implement search functionality
    
    @on(DataTable.RowSelected)
    def on_datatable_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection in the content table."""
        # Get the selected row
        row = event.data_table.get_row(event.row_key)
        if not row:
            return
        
        # Get the content ID from the first column
        content_id = int(row[0])
        self.logger.info(f"Selected content ID: {content_id}")
        
        # Load the content details
        self.load_content_details(content_id)
    
    def load_content_details(self, content_id: int) -> None:
        """Load content details for the given ID."""
        self.logger.info(f"Loading content details for ID: {content_id}")
        
        # Store the current content ID
        self.current_content_id = content_id
        
        # Get the content from the database
        content = self.db.get_content(content_id)
        if not content:
            self.logger.error(f"Content not found for ID: {content_id}")
            return
        
        # Switch to details tab
        tabs = self.query_one(Tabs)
        tabs.active = "details-tab"
        
        # Create markdown content
        markdown = f"""# {content.title}

## Metadata
- **Type:** {content.content_type.value}
- **URL:** {content.url}
- **Extracted:** {content.extracted_at.strftime('%Y-%m-%d %H:%M:%S') if content.extracted_at else 'N/A'}
- **Pattern:** {content.extraction_pattern}

## Content
{content.content}
"""
        
        # Update the markdown viewer
        markdown_viewer = self.query_one("#content-details", MarkdownViewer)
        markdown_viewer.update(markdown)
    
    @on(Button.Pressed, "#extract-button")
    def on_extract_button_pressed(self, event: Button.Pressed) -> None:
        """Handle extract button press."""
        self.logger.info("Extract button pressed")
        
        # Get the URL
        url_input = self.query_one("#extract-url", Input)
        url = url_input.value.strip()
        if not url:
            self.notify("Please enter a URL", severity="error")
            return
        
        # Get the content type
        content_type_select = self.query_one("#content-type", Select)
        content_type_str = content_type_select.value
        try:
            content_type = ContentType(content_type_str)
        except ValueError:
            self.notify(f"Invalid content type: {content_type_str}", severity="error")
            return
        
        # Get the extraction pattern
        pattern_select = self.query_one("#extraction-pattern", Select)
        pattern = pattern_select.value
        
        # Get the LLM provider
        provider_select = self.query_one("#llm-provider", Select)
        provider = provider_select.value
        
        # Disable the button while extracting
        event.button.disabled = True
        
        # Start the extraction
        self.extract_content(url, content_type, pattern, provider)
        
        # Re-enable the button
        event.button.disabled = False
    
    @work(thread=True)
    def extract_content(self, url: str, content_type: ContentType, pattern: str, provider: str) -> None:
        """Extract content from the given URL."""
        self.logger.info(f"Extracting content from {url} using {pattern} pattern with {provider} provider")
        
        try:
            # Create content shell based on content type
            if content_type == ContentType.YOUTUBE:
                # Extract video ID from URL
                video_id = extract_video_id(url)
                if not video_id:
                    self.call_from_thread(self.notify, f"Invalid YouTube URL: {url}", severity="error")
                    return
                
                # Create content shell
                content = create_youtube_content_shell(url, video_id)
            elif content_type == ContentType.ARTICLE:
                # Create content shell
                content = create_article_content_shell(url)
            else:
                self.call_from_thread(self.notify, f"Unsupported content type: {content_type}", severity="error")
                return
            
            # Create extractor
            extractor = ContentExtractor(provider=provider)
            
            # Extract content
            content = extractor.extract(content, pattern)
            
            # Save to database
            content_id = self.db.add_content(content)
            
            # Refresh the content list
            self.call_from_thread(self.refresh_content_list)
            
            # Show success message
            self.call_from_thread(self.notify, f"Content extracted successfully (ID: {content_id})", severity="information")
            
            # Load the content details
            if content:
                # Switch to details tab
                tabs = self.query_one(Tabs)
                self.call_from_thread(setattr, tabs, "active", "details-tab")
                
                # Create markdown content
                markdown = f"""# {content.title}

## Metadata
- **Type:** {content.content_type.value}
- **URL:** {content.url}
- **Extracted:** {content.extracted_at.strftime('%Y-%m-%d %H:%M:%S') if content.extracted_at else 'N/A'}
- **Pattern:** {content.extraction_pattern}

## Content
{content.content}
"""
                
                # Update the markdown viewer
                markdown_viewer = self.query_one("#content-details", MarkdownViewer)
                self.call_from_thread(markdown_viewer.update, markdown)
        except Exception as e:
            self.logger.error(f"Error extracting content: {e}")
            self.call_from_thread(self.notify, f"Error extracting content: {str(e)}", severity="error")
    
    @on(Button.Pressed, "#extract-clear-button")
    def on_extract_clear_button_pressed(self, event: Button.Pressed) -> None:
        """Handle extract clear button press."""
        self.logger.info("Extract clear button pressed")
        
        # Clear the URL input
        url_input = self.query_one("#extract-url", Input)
        url_input.value = ""
        
        # Focus the URL input
        url_input.focus()
    
    @on(Button.Pressed, "#stitch-create-button")
    def on_stitch_create_button_pressed(self, event: Button.Pressed) -> None:
        """Handle stitch create button press."""
        self.logger.info("Stitch create button pressed")
        
        # Get the name
        name_input = self.query_one("#stitch-name", Input)
        name = name_input.value.strip()
        if not name:
            self.notify("Please enter a name", severity="error")
            return
        
        # Get the description
        description_input = self.query_one("#stitch-description", Input)
        description = description_input.value.strip()
        
        # Get the LLM provider
        provider_select = self.query_one("#stitch-provider", Select)
        provider = provider_select.value
        
        # Disable the button while creating
        event.button.disabled = True
        
        # Create the stitch
        stitch = Stitch(
            name=name,
            description=description,
            provider=provider,
            steps=[]
        )
        
        # Add to database
        stitch_id = add_stitch(stitch)
        
        # Show success message
        self.notify(f"Stitch created successfully (ID: {stitch_id})", severity="information")
        
        # Clear the form
        name_input.value = ""
        description_input.value = ""
        
        # Re-enable the button
        event.button.disabled = False
    
    @on(Button.Pressed, "#stitch-clear-button")
    def on_stitch_clear_button_pressed(self, event: Button.Pressed) -> None:
        """Handle stitch clear button press."""
        self.logger.info("Stitch clear button pressed")
        
        # Clear the inputs
        name_input = self.query_one("#stitch-name", Input)
        name_input.value = ""
        
        description_input = self.query_one("#stitch-description", Input)
        description_input.value = ""
        
        # Focus the name input
        name_input.focus()
    
    @on(Button.Pressed, "#settings-save-button")
    def on_settings_save_button_pressed(self, event: Button.Pressed) -> None:
        """Handle settings save button press."""
        self.logger.info("Settings save button pressed")
        
        # Get the default provider
        provider_select = self.query_one("#default-provider", Select)
        provider = provider_select.value
        
        # Update the default provider
        self.default_provider = provider
        
        # Show success message
        self.notify(f"Settings saved successfully", severity="information")
    
    @on(Button.Pressed, "#settings-reset-button")
    def on_settings_reset_button_pressed(self, event: Button.Pressed) -> None:
        """Handle settings reset button press."""
        self.logger.info("Settings reset button pressed")
        
        # Reset the default provider
        provider_select = self.query_one("#default-provider", Select)
        provider_select.value = os.getenv("DEFAULT_LLM_PROVIDER", "mistral")
    
    def new_extract(self) -> None:
        """Create a new extract."""
        self.logger.info("Creating new extract")
        
        try:
            # First, check if the extract tab exists
            tabs = self.query_one(Tabs)
            tab_ids = [tab.id for tab in tabs.query("TabPane")]
            
            if "extract-tab" not in tab_ids:
                self.logger.error(f"Extract tab not found. Available tabs: {tab_ids}")
                self.notify("Error: Extract tab not found", severity="error")
                return
            
            # Switch to the extract tab
            tabs.active = "extract-tab"
            
            # Make sure the tab is fully rendered
            self.refresh()
            
            # Use a longer delay to ensure the tab is fully rendered
            self.set_timer(1.0, self._ensure_extract_tab_ready)
        except Exception as e:
            self.logger.error(f"Error in new_extract: {e}")
            self.notify(f"Error: {str(e)}", severity="error")


def run_tui():
    """Run the TUI application."""
    logging.getLogger("run_tui").info("Starting TUI application")
    app = ExtractApp()
    app.run()


if __name__ == "__main__":
    run_tui()
