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
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("n", "new_extract", "New Extract"),
        ("r", "refresh", "Refresh"),
        ("f", "focus_search", "Search"),
        ("s", "new_stitch", "New Stitch"),
    ]
    
    def __init__(self):
        """Initialize the application."""
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
        """Compose the UI layout."""
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
                yield Tabs(
                    TabPane("Details", id="details-tab"),
                    TabPane("Extract", id="extract-tab"),
                    TabPane("Stitch", id="stitch-tab"),
                    TabPane("Settings", id="settings-tab"),
                )
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Set up the UI when the app is mounted."""
        self.logger.info("Mounting app")
        
        # Set up content table
        table = self.query_one("#content-table", DataTable)
        table.add_columns("ID", "Title", "Type", "Date", "Pattern")
        
        # Load initial data
        self.refresh_content_list()
        
        # Set up details tab
        details_tab = self.query_one("#details-tab", TabPane)
        details_tab.mount(MarkdownViewer(id="content-details", classes="content-details"))
        
        # Set up extract tab
        extract_tab = self.query_one("#extract-tab", TabPane)
        with extract_tab:
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
        
        # Set up stitch tab
        stitch_tab = self.query_one("#stitch-tab", TabPane)
        with stitch_tab:
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
        
        # Set up settings tab
        settings_tab = self.query_one("#settings-tab", TabPane)
        with settings_tab:
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
        
        # Log that the app is mounted
        self.logger.info("App mounted successfully")
    
    def _get_stitch_options(self) -> List[tuple]:
        """Get options for stitch select."""
        stitches = self.db.get_all_stitches()
        options = []
        
        # Add option to create a custom stitch
        options.append(("custom", "Custom (comma-separated patterns)"))
        
        # Add saved stitches
        for stitch in stitches:
            options.append((str(stitch.id), stitch.name))
        
        return options
    
    def refresh_content_list(self) -> None:
        """Refresh the content list from the database."""
        table = self.query_one("#content-table", DataTable)
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
    
    def action_refresh(self) -> None:
        """Refresh the content list."""
        self.refresh_content_list()
    
    def action_new_extract(self) -> None:
        """Focus the extract tab."""
        self.logger.info("Action: new_extract")
        
        # First, switch to the extract tab
        tabs = self.query_one(Tabs)
        tabs.active = "extract-tab"
        
        # Use a longer delay to ensure the tab is fully rendered
        self.set_timer(1.0, self._ensure_extract_tab_ready)
    
    def _ensure_extract_tab_ready(self) -> None:
        """Ensure the extract tab is ready and then focus the URL input."""
        # Check if we're on the extract tab
        tabs = self.query_one(Tabs)
        if tabs.active != "extract-tab":
            self.logger.error("Extract tab is not active, cannot proceed")
            return
            
        # Try to find the extract tab content
        try:
            extract_tab = self.query_one("#extract-tab", TabPane)
            
            # Check if the tab has been populated with content
            inputs = extract_tab.query("Input")
            if not inputs:
                self.logger.error("Extract tab has no input elements, waiting for UI to update")
                # Try again after a delay
                self.set_timer(0.5, self._ensure_extract_tab_ready)
                return
                
            # Find the URL input specifically
            url_input = None
            for input_elem in inputs:
                if input_elem.id == "url-input":
                    url_input = input_elem
                    break
                    
            if url_input:
                url_input.focus()
                self.logger.info("Successfully focused URL input")
            else:
                self.logger.error("URL input not found in extract tab")
        except Exception as e:
            self.logger.error(f"Error while focusing URL input: {e}")
            # Try again after a delay
            self.set_timer(0.5, self._ensure_extract_tab_ready)
    
    def action_new_stitch(self) -> None:
        """Focus the stitch tab."""
        self.logger.info("Action: new_stitch")
        
        # First, switch to the stitch tab
        tabs = self.query_one(Tabs)
        tabs.active = "stitch-tab"
        
        # Use a longer delay to ensure the tab is fully rendered
        self.set_timer(1.0, self._ensure_stitch_tab_ready)
    
    def _ensure_stitch_tab_ready(self) -> None:
        """Ensure the stitch tab is ready and then focus the URL input."""
        # Check if we're on the stitch tab
        tabs = self.query_one(Tabs)
        if tabs.active != "stitch-tab":
            self.logger.error("Stitch tab is not active, cannot proceed")
            return
            
        # Try to find the stitch tab content
        try:
            stitch_tab = self.query_one("#stitch-tab", TabPane)
            
            # Check if the tab has been populated with content
            inputs = stitch_tab.query("Input")
            if not inputs:
                self.logger.error("Stitch tab has no input elements, waiting for UI to update")
                # Try again after a delay
                self.set_timer(0.5, self._ensure_stitch_tab_ready)
                return
                
            # Find the URL input specifically
            url_input = None
            for input_elem in inputs:
                if input_elem.id == "stitch-url-input":
                    url_input = input_elem
                    break
                    
            if url_input:
                url_input.focus()
                self.logger.info("Successfully focused stitch URL input")
            else:
                self.logger.error("Stitch URL input not found in stitch tab")
        except Exception as e:
            self.logger.error(f"Error while focusing stitch URL input: {e}")
            # Try again after a delay
            self.set_timer(0.5, self._ensure_stitch_tab_ready)
    
    def action_focus_search(self) -> None:
        """Focus the search input."""
        search_input = self.query_one("#search-input", Input)
        search_input.focus()
    
    @on(DataTable.RowSelected)
    def show_content_details(self, event: DataTable.RowSelected) -> None:
        """Show content details when a row is selected."""
        # Get content ID from the first cell
        content_id = int(event.data_table.get_cell_at((event.row_key, 0)))
        self.current_content_id = content_id
        
        # Get content from database
        content = self.db.get_content(content_id)
        if not content:
            return
        
        # Switch to details tab
        tabs = self.query_one(Tabs)
        tabs.active = "details-tab"
        
        # Create markdown content
        markdown = f"# {content.title}\n\n"
        markdown += f"**Source:** [{content.url}]({content.url})  \n"
        markdown += f"**Type:** {content.content_type.value}  \n"
        markdown += f"**Extracted:** {content.extracted_at.strftime('%Y-%m-%d %H:%M:%S') if content.extracted_at else 'Unknown'}  \n"
        markdown += f"**Pattern:** {content.extraction_pattern}  \n"
        markdown += f"**Provider:** {content.extraction_provider.value}  \n"
        markdown += f"**Model:** {content.extraction_model}  \n"
        
        if content.tags:
            markdown += f"**Tags:** {', '.join(content.tags)}  \n"
        
        if content.stitch_id:
            markdown += f"**Stitch ID:** {content.stitch_id}, Step: {content.stitch_step}  \n"
        
        markdown += "\n## Summary\n\n"
        markdown += content.summary
        
        if content.key_insights:
            markdown += "\n\n## Key Insights\n\n"
            for insight in content.key_insights:
                markdown += f"- {insight}\n"
        
        if content.main_points:
            markdown += "\n\n## Main Points\n\n"
            for point in content.main_points:
                markdown += f"- {point}\n"
        
        if content.quotes:
            markdown += "\n\n## Notable Quotes\n\n"
            for quote in content.quotes:
                markdown += f"> {quote}\n\n"
        
        if content.questions_raised:
            markdown += "\n\n## Questions Raised\n\n"
            for question in content.questions_raised:
                markdown += f"- {question}\n"
        
        if content.action_items:
            markdown += "\n\n## Action Items\n\n"
            for item in content.action_items:
                markdown += f"- {item}\n"
        
        # Update markdown viewer
        markdown_viewer = self.query_one("#content-details", MarkdownViewer)
        markdown_viewer.document = markdown
    
    @on(Button.Pressed, "#search-button")
    def search_content(self) -> None:
        """Search for content."""
        search_input = self.query_one("#search-input", Input)
        query = search_input.value
        
        table = self.query_one("#content-table", DataTable)
        table.clear()
        
        # Get content from database
        results = self.db.search_content(query=query, limit=100)
        
        # Add to table
        for content in results:
            table.add_row(
                str(content.id),
                content.title[:50] + ("..." if len(content.title) > 50 else ""),
                content.content_type.value,
                content.extracted_at.strftime("%Y-%m-%d") if content.extracted_at else "",
                content.extraction_pattern
            )
    
    @on(Button.Pressed, "#new-button")
    def new_extract(self) -> None:
        """Switch to extract tab."""
        # Use the same approach as action_new_extract
        tabs = self.query_one(Tabs)
        tabs.active = "extract-tab"
        
        # Use a longer delay to ensure the tab is fully rendered
        self.set_timer(1.0, self._ensure_extract_tab_ready)
    
    def _focus_url_input(self, retry_count=0) -> None:
        """Focus the URL input after a short delay."""
        # Limit retries to prevent infinite recursion
        if retry_count >= 5:
            self.logger.error("Failed to focus URL input after multiple attempts")
            return
            
        try:
            # Check if the tab is active before trying to focus
            tabs = self.query_one(Tabs)
            if tabs.active != "extract-tab":
                self.logger.error("Extract tab is not active, cannot focus input")
                # Try again with incremented retry count after a longer delay
                self.set_timer(0.5, lambda: self._focus_url_input(retry_count + 1))
                return
            
            # Check if the input element exists
            inputs = self.query("Input")
            url_input = None
            for input_elem in inputs:
                if input_elem.id == "url-input":
                    url_input = input_elem
                    break
                    
            if not url_input:
                self.logger.error("URL input element not found, waiting for UI to update")
                # Try again with incremented retry count after a longer delay
                self.set_timer(0.5, lambda: self._focus_url_input(retry_count + 1))
                return
                
            url_input.focus()
            self.logger.info("Focused URL input")
        except Exception as e:
            self.logger.error(f"Failed to focus URL input: {e}")
            # Try again with incremented retry count after a longer delay
            self.set_timer(0.5, lambda: self._focus_url_input(retry_count + 1))
            
    def _focus_stitch_url_input(self, retry_count=0) -> None:
        """Focus the stitch URL input after a short delay."""
        # Limit retries to prevent infinite recursion
        if retry_count >= 5:
            self.logger.error("Failed to focus stitch URL input after multiple attempts")
            return
            
        try:
            # Check if the tab is active before trying to focus
            tabs = self.query_one(Tabs)
            if tabs.active != "stitch-tab":
                self.logger.error("Stitch tab is not active, cannot focus input")
                # Try again with incremented retry count after a longer delay
                self.set_timer(0.5, lambda: self._focus_stitch_url_input(retry_count + 1))
                return
            
            # Check if the input element exists
            inputs = self.query("Input")
            url_input = None
            for input_elem in inputs:
                if input_elem.id == "stitch-url-input":
                    url_input = input_elem
                    break
                    
            if not url_input:
                self.logger.error("Stitch URL input element not found, waiting for UI to update")
                # Try again with incremented retry count after a longer delay
                self.set_timer(0.5, lambda: self._focus_stitch_url_input(retry_count + 1))
                return
                
            url_input.focus()
            self.logger.info("Focused stitch URL input")
        except Exception as e:
            self.logger.error(f"Failed to focus stitch URL input: {e}")
            # Try again with incremented retry count after a longer delay
            self.set_timer(0.5, lambda: self._focus_stitch_url_input(retry_count + 1))
    
    @on(Button.Pressed, "#extract-button")
    def start_extraction(self) -> None:
        """Start the extraction process."""
        url_input = self.query_one("#url-input", Input)
        content_type_select = self.query_one("#content-type-select", Select)
        pattern_select = self.query_one("#pattern-select", Select)
        provider_select = self.query_one("#provider-select", Select)
        status = self.query_one("#extract-status", Static)
        
        url = url_input.value
        content_type = content_type_select.value
        pattern = pattern_select.value
        provider = provider_select.value
        
        if not url:
            status.update("Please enter a URL")
            status.add_class("error-message")
            return
        
        # Check provider
        if not provider:
            status.update("Please select a provider")
            status.add_class("error-message")
            return
        
        # Start extraction
        status.update("Extracting content...")
        status.remove_class("error-message")
        status.add_class("status-message")
        
        # Run extraction in background
        self.extract_content_background(url, content_type, pattern, provider)
    
    @work(thread=True)
    def extract_content_background(self, url: str, content_type: str, pattern: str, provider: str) -> None:
        """Extract content in the background."""
        status = self.query_one("#extract-status", Static)
        
        try:
            # Create content shell based on type
            if content_type == "youtube":
                # Validate YouTube URL
                if not extract_video_id(url):
                    if len(url) == 11:  # Might be just the video ID
                        url = f"https://www.youtube.com/watch?v={url}"
                    else:
                        self.call_from_thread(status.update, "Invalid YouTube URL or video ID")
                        self.call_from_thread(status.remove_class, "status-message")
                        self.call_from_thread(status.add_class, "error-message")
                        return
                
                self.call_from_thread(status.update, "Fetching video information...")
                content = create_youtube_content_shell(url, provider=LLMProvider(provider))
            else:  # article
                self.call_from_thread(status.update, "Fetching article information...")
                content = create_article_content_shell(url, provider=LLMProvider(provider))
            
            # Extract content
            self.call_from_thread(status.update, "Extracting insights...")
            extractor = ContentExtractor(provider_name=provider)
            content = extractor.extract_content(content, pattern_name=pattern)
            
            # Save to database
            self.call_from_thread(status.update, "Saving to database...")
            content_id = self.db.save_content(content)
            
            # Update UI
            self.call_from_thread(self.refresh_content_list)
            self.call_from_thread(status.update, f"Extraction complete! Content ID: {content_id}")
            self.call_from_thread(status.remove_class, "status-message")
            self.call_from_thread(status.add_class, "success-message")
            
            # Clear input
            url_input = self.query_one("#url-input", Input)
            self.call_from_thread(url_input.clear)
            
            # Select the new content
            self.current_content_id = content_id
            
            # Show the content details
            content = self.db.get_content(content_id)
            if content:
                # Switch to details tab
                tabs = self.query_one(Tabs)
                self.call_from_thread(setattr, tabs, "active", "details-tab")
                
                # Create markdown content
                markdown = f"# {content.title}\n\n"
                markdown += f"**Source:** [{content.url}]({content.url})  \n"
                markdown += f"**Type:** {content.content_type.value}  \n"
                markdown += f"**Extracted:** {content.extracted_at.strftime('%Y-%m-%d %H:%M:%S') if content.extracted_at else 'Unknown'}  \n"
                markdown += f"**Pattern:** {content.extraction_pattern}  \n"
                markdown += f"**Provider:** {content.extraction_provider.value}  \n"
                markdown += f"**Model:** {content.extraction_model}  \n"
                
                if content.tags:
                    markdown += f"**Tags:** {', '.join(content.tags)}  \n"
                
                markdown += "\n## Summary\n\n"
                markdown += content.summary
                
                if content.key_insights:
                    markdown += "\n\n## Key Insights\n\n"
                    for insight in content.key_insights:
                        markdown += f"- {insight}\n"
                
                if content.main_points:
                    markdown += "\n\n## Main Points\n\n"
                    for point in content.main_points:
                        markdown += f"- {point}\n"
                
                if content.quotes:
                    markdown += "\n\n## Notable Quotes\n\n"
                    for quote in content.quotes:
                        markdown += f"> {quote}\n\n"
                
                if content.questions_raised:
                    markdown += "\n\n## Questions Raised\n\n"
                    for question in content.questions_raised:
                        markdown += f"- {question}\n"
                
                if content.action_items:
                    markdown += "\n\n## Action Items\n\n"
                    for item in content.action_items:
                        markdown += f"- {item}\n"
                
                # Update markdown viewer
                markdown_viewer = self.query_one("#content-details", MarkdownViewer)
                self.call_from_thread(setattr, markdown_viewer, "document", markdown)
        
        except Exception as e:
            self.call_from_thread(status.update, f"Error: {str(e)}")
            self.call_from_thread(status.remove_class, "status-message")
            self.call_from_thread(status.add_class, "error-message")
    
    @on(Button.Pressed, "#run-stitch-button")
    def run_stitch(self) -> None:
        """Run a stitch on a URL."""
        url_input = self.query_one("#stitch-url-input", Input)
        stitch_select = self.query_one("#stitch-select", Select)
        provider_select = self.query_one("#stitch-provider-select", Select)
        status = self.query_one("#stitch-status", Static)
        
        url = url_input.value
        stitch_id = stitch_select.value
        provider = provider_select.value
        
        if not url:
            status.update("Please enter a URL")
            status.add_class("error-message")
            return
        
        if not provider:
            status.update("Please select a provider")
            status.add_class("error-message")
            return
        
        # If custom stitch, show input dialog
        if stitch_id == "custom":
            # TODO: Implement custom stitch input dialog
            status.update("Custom stitches not yet implemented in TUI")
            status.add_class("error-message")
            return
        
        # Start stitch execution
        status.update("Running stitch...")
        status.remove_class("error-message")
        status.add_class("status-message")
        
        # Run stitch in background
        self.run_stitch_background(url, int(stitch_id), provider)
    
    @work(thread=True)
    def run_stitch_background(self, url: str, stitch_id: int, provider: str) -> None:
        """Run a stitch in the background."""
        status = self.query_one("#stitch-status", Static)
        
        try:
            # Determine content type
            is_youtube = extract_video_id(url) is not None
            
            # Create content shell
            self.call_from_thread(status.update, "Fetching content information...")
            if is_youtube:
                content = create_youtube_content_shell(url, provider=LLMProvider(provider))
            else:
                content = create_article_content_shell(url, provider=LLMProvider(provider))
            
            # Get stitch
            stitch = self.db.get_stitch(stitch_id)
            if not stitch:
                self.call_from_thread(status.update, f"Stitch with ID {stitch_id} not found")
                self.call_from_thread(status.remove_class, "status-message")
                self.call_from_thread(status.add_class, "error-message")
                return
            
            # Run stitch
            self.call_from_thread(status.update, f"Running stitch: {stitch.name}...")
            executor = StitchExecutor(provider_name=provider)
            result = executor.execute_stitch(stitch, content)
            
            # Save to database
            self.call_from_thread(status.update, "Saving to database...")
            content_id = self.db.save_content(result)
            
            # Update UI
            self.call_from_thread(self.refresh_content_list)
            self.call_from_thread(status.update, f"Stitch execution complete! Content ID: {content_id}")
            self.call_from_thread(status.remove_class, "status-message")
            self.call_from_thread(status.add_class, "success-message")
            
            # Clear input
            url_input = self.query_one("#stitch-url-input", Input)
            self.call_from_thread(url_input.clear)
            
            # Select the new content
            self.current_content_id = content_id
            
            # Show the content details
            content = self.db.get_content(content_id)
            if content:
                # Switch to details tab
                tabs = self.query_one(Tabs)
                self.call_from_thread(setattr, tabs, "active", "details-tab")
                
                # Create markdown content
                markdown = f"# {content.title}\n\n"
                markdown += f"**Source:** [{content.url}]({content.url})  \n"
                markdown += f"**Type:** {content.content_type.value}  \n"
                markdown += f"**Extracted:** {content.extracted_at.strftime('%Y-%m-%d %H:%M:%S') if content.extracted_at else 'Unknown'}  \n"
                markdown += f"**Pattern:** {content.extraction_pattern}  \n"
                markdown += f"**Provider:** {content.extraction_provider.value}  \n"
                markdown += f"**Model:** {content.extraction_model}  \n"
                
                if content.tags:
                    markdown += f"**Tags:** {', '.join(content.tags)}  \n"
                
                if content.stitch_id:
                    markdown += f"**Stitch ID:** {content.stitch_id}, Step: {content.stitch_step}  \n"
                
                markdown += "\n## Summary\n\n"
                markdown += content.summary
                
                if content.key_insights:
                    markdown += "\n\n## Key Insights\n\n"
                    for insight in content.key_insights:
                        markdown += f"- {insight}\n"
                
                if content.main_points:
                    markdown += "\n\n## Main Points\n\n"
                    for point in content.main_points:
                        markdown += f"- {point}\n"
                
                if content.quotes:
                    markdown += "\n\n## Notable Quotes\n\n"
                    for quote in content.quotes:
                        markdown += f"> {quote}\n\n"
                
                if content.questions_raised:
                    markdown += "\n\n## Questions Raised\n\n"
                    for question in content.questions_raised:
                        markdown += f"- {question}\n"
                
                if content.action_items:
                    markdown += "\n\n## Action Items\n\n"
                    for item in content.action_items:
                        markdown += f"- {item}\n"
                
                # Update markdown viewer
                markdown_viewer = self.query_one("#content-details", MarkdownViewer)
                self.call_from_thread(setattr, markdown_viewer, "document", markdown)
        
        except Exception as e:
            self.call_from_thread(status.update, f"Error: {str(e)}")
            self.call_from_thread(status.remove_class, "status-message")
            self.call_from_thread(status.add_class, "error-message")
    
    @on(Button.Pressed, "#create-stitch-button")
    def show_create_stitch_dialog(self) -> None:
        """Show dialog to create a new stitch."""
        # TODO: Implement create stitch dialog
        status = self.query_one("#stitch-status", Static)
        status.update("Create stitch dialog not yet implemented in TUI")
        status.add_class("error-message")
    
    @on(Button.Pressed, "#save-settings-button")
    def save_settings(self) -> None:
        """Save settings."""
        default_provider_select = self.query_one("#default-provider-select", Select)
        status = self.query_one("#settings-status", Static)
        
        # Save default provider to environment variable
        self.default_provider = default_provider_select.value
        os.environ["DEFAULT_LLM_PROVIDER"] = self.default_provider
        
        status.update("Settings saved!")
        status.add_class("success-message")

def run_tui() -> None:
    """Run the TUI application."""
    logger = logging.getLogger("run_tui")
    logger.info("Starting TUI application")
    try:
        app = ExtractApp()
        app.run()
    except Exception as e:
        logger.error(f"Error running TUI application: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    run_tui()
