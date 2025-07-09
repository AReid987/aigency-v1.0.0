"""Text User Interface for AIgency Extract."""

import os
from datetime import datetime
from typing import Dict, List, Optional

from rich.text import Text
from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import (Button, DataTable, Footer, Header, Input, Label,
                            MarkdownViewer, Select, Static, TabPane, Tabs)

from aigency_extract.data.database import ExtractDatabase
from aigency_extract.data.models import ContentType
from aigency_extract.utils.article import create_article_content_shell
from aigency_extract.utils.extraction import ContentExtractor, ExtractionPatterns
from aigency_extract.utils.youtube import create_youtube_content_shell, extract_video_id


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
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("n", "new_extract", "New Extract"),
        ("r", "refresh", "Refresh"),
        ("f", "focus_search", "Search"),
    ]
    
    def __init__(self):
        """Initialize the application."""
        super().__init__()
        self.db = ExtractDatabase()
        self.current_content_id = None
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
    
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
                    TabPane("Settings", id="settings-tab"),
                )
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Set up the UI when the app is mounted."""
        # Set up content table
        table = self.query_one("#content-table", DataTable)
        table.add_columns("ID", "Title", "Type", "Date", "Tags")
        
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
                        [(pattern, pattern) for pattern in ExtractionPatterns.get_all_patterns()],
                        id="pattern-select",
                        value=ExtractionPatterns.YOUTUBE_SUMMARY,
                        classes="form-input"
                    )
                
                with Horizontal(classes="button-container"):
                    yield Button("Extract", id="extract-button", variant="primary")
                
                yield Static("", id="extract-status", classes="status-message")
        
        # Set up settings tab
        settings_tab = self.query_one("#settings-tab", TabPane)
        with settings_tab:
            with Container(classes="extraction-form"):
                with Horizontal(classes="form-row"):
                    yield Label("OpenAI API Key:", classes="form-label")
                    yield Input(
                        placeholder="sk-...",
                        id="api-key-input",
                        password=True,
                        value=self.api_key,
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
                ", ".join(content.tags[:3]) + ("..." if len(content.tags) > 3 else "")
            )
    
    def action_refresh(self) -> None:
        """Refresh the content list."""
        self.refresh_content_list()
    
    def action_new_extract(self) -> None:
        """Focus the extract tab."""
        tabs = self.query_one(Tabs)
        tabs.active = "extract-tab"
        url_input = self.query_one("#url-input", Input)
        url_input.focus()
    
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
                ", ".join(content.tags[:3]) + ("..." if len(content.tags) > 3 else "")
            )
    
    @on(Button.Pressed, "#new-button")
    def new_extract(self) -> None:
        """Switch to extract tab."""
        self.action_new_extract()
    
    @on(Button.Pressed, "#extract-button")
    def start_extraction(self) -> None:
        """Start the extraction process."""
        url_input = self.query_one("#url-input", Input)
        content_type_select = self.query_one("#content-type-select", Select)
        pattern_select = self.query_one("#pattern-select", Select)
        status = self.query_one("#extract-status", Static)
        
        url = url_input.value
        content_type = content_type_select.value
        pattern = pattern_select.value
        
        if not url:
            status.update("Please enter a URL")
            status.add_class("error-message")
            return
        
        # Check API key
        api_key_input = self.query_one("#api-key-input", Input)
        api_key = api_key_input.value
        
        if not api_key:
            status.update("Please enter an OpenAI API key in Settings")
            status.add_class("error-message")
            return
        
        # Start extraction
        status.update("Extracting content...")
        status.remove_class("error-message")
        status.add_class("status-message")
        
        # Run extraction in background
        self.extract_content_background(url, content_type, pattern, api_key)
    
    @work
    def extract_content_background(self, url: str, content_type: str, pattern: str, api_key: str) -> None:
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
                content = create_youtube_content_shell(url)
            else:  # article
                self.call_from_thread(status.update, "Fetching article information...")
                content = create_article_content_shell(url)
            
            # Extract content
            self.call_from_thread(status.update, "Extracting insights...")
            extractor = ContentExtractor(api_key=api_key)
            content = extractor.extract_content(content, pattern=pattern)
            
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
    
    @on(Button.Pressed, "#save-settings-button")
    def save_settings(self) -> None:
        """Save settings."""
        api_key_input = self.query_one("#api-key-input", Input)
        status = self.query_one("#settings-status", Static)
        
        # Save API key to environment variable
        self.api_key = api_key_input.value
        os.environ["OPENAI_API_KEY"] = self.api_key
        
        status.update("Settings saved!")
        status.add_class("success-message")


def run_tui() -> None:
    """Run the TUI application."""
    app = ExtractApp()
    app.run()
