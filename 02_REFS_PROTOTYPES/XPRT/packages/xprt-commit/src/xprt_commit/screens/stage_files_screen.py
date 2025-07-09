# Filename: packages/xprt-commit/src/xprt_commit/screens/stage_files_screen.py
# Path: packages/xprt-commit/src/xprt_commit/screens
# Created Date: Tuesday, April 22nd 2025, 4:10:00 am
# Author: Roo
#
# Copyright (c) 2025 10xAigency

import logging
from typing import List, Dict, Tuple

from textual.app import ComposeResult, RenderResult
from textual.binding import Binding
from textual.containers import VerticalScroll, Container, Horizontal
from textual.screen import Screen, ModalScreen
from textual.widgets import Header, Footer, DataTable, Button, Static, Checkbox, Label
from textual.reactive import reactive

# Assuming git_utils is accessible, adjust import if necessary
from ..git_utils import stage_files, get_staged_files, get_unstaged_files # Added get_unstaged_files

log = logging.getLogger(__name__)

class StageFilesScreen(ModalScreen[Tuple[bool, List[str]]]):
    """
    A modal screen to display unstaged files and allow the user to stage them.
    Returns a tuple: (staging_attempted: bool, newly_staged_files: List[str])
    """

    BINDINGS = [
        Binding(key="s", action="stage_selected", description="Stage Selected"),
        Binding(key="k", action="skip_staging", description="Skip Staging"),
        Binding(key="q", action="quit_app", description="Quit"),
    ]

    DEFAULT_CSS = """
    StageFilesScreen {
        align: center middle;
    }

    #stage-dialog {
        width: 80%;
        max-width: 90;
        height: 80%;
        max-height: 30;
        border: thick $accent;
        background: $surface;
    }

    #stage-status {
        height: auto;
        dock: top;
        padding: 0 1;
    }

    #stage-table {
        height: 1fr;
        margin-bottom: 1;
        border: thin $accent;
    }

    #stage-buttons {
        align: center middle;
        height: auto;
        margin-top: 1;
        dock: bottom;
    }

    Label {
        margin: 1 0 0 1;
    }
    """

    staged_count = reactive(0)
    unstaged_count = reactive(0)

    def __init__(self, unstaged_files: List[Dict[str, str]], name: str | None = None, id: str | None = None, classes: str | None = None):
        super().__init__(name=name, id=id, classes=classes)
        self.unstaged_files_data = unstaged_files
        # Store checkbox references mapped to file data
        self._checkboxes: Dict[Checkbox, Dict[str, str]] = {}


    def compose(self) -> ComposeResult:
        with Container(id="stage-dialog"):
            yield Label("Unstaged files found. Select files to stage:")
            # Add status display
            with Horizontal(id="stage-status"):
                yield Static(f"Staged: {self.staged_count}", id="staged-count-label")
                yield Static(f"Unstaged: {self.unstaged_count}", id="unstaged-count-label")
            with VerticalScroll():
                yield DataTable(id="stage-table", cursor_type="row", zebra_stripes=True)
            with Container(id="stage-buttons"):
                yield Button("Stage Selected", variant="primary", id="stage-selected-btn")
                yield Button("Stage All", id="stage-all-btn")
                yield Button("Skip Staging / Continue", id="skip-btn")
            yield Footer() # Inherits bindings from the screen

    # Helper method to update counts and table
    def _update_file_status(self) -> None:
        log.info("Updating file status...")
        try:
            # Use the imported git_utils functions
            current_staged = get_staged_files()
            current_unstaged = get_unstaged_files()

            self.staged_count = len(current_staged)
            self.unstaged_count = len(current_unstaged)
            self.unstaged_files_data = current_unstaged # Update internal data

            log.info(f"Updated counts: Staged={self.staged_count}, Unstaged={self.unstaged_count}")

            # Update labels
            staged_label = self.query_one("#staged-count-label", Static)
            unstaged_label = self.query_one("#unstaged-count-label", Static)
            staged_label.update(f"Staged: {self.staged_count}")
            unstaged_label.update(f"Unstaged: {self.unstaged_count}")

            # Update table
            table = self.query_one(DataTable)
            table.clear()
            self._checkboxes.clear() # Clear old checkbox references

            for file_info in self.unstaged_files_data:
                checkbox = Checkbox("", value=False)
                self._checkboxes[checkbox] = file_info
                table.add_row(
                    checkbox,
                    file_info['status'],
                    file_info['file'],
                    key=file_info['file']
                )

            # Disable buttons if no unstaged files left
            has_unstaged = bool(self.unstaged_files_data)
            self.query_one("#stage-selected-btn", Button).disabled = not has_unstaged
            self.query_one("#stage-all-btn", Button).disabled = not has_unstaged

            if not has_unstaged:
                table.add_row(Static("All changes staged or no unstaged files."), Static(""), Static(""))

        except Exception as e:
            log.error(f"Error updating file status: {e}", exc_info=True)
            self.app.notify(f"Error updating file status: {e}", severity="error")

    def watch_staged_count(self, count: int) -> None:
        """Called when staged_count changes."""
        label = self.query_one("#staged-count-label", Static)
        label.update(f"Staged: {count}")

    def watch_unstaged_count(self, count: int) -> None:
        """Called when unstaged_count changes."""
        label = self.query_one("#unstaged-count-label", Static)
        label.update(f"Unstaged: {count}")

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        log.info("StageFilesScreen mounted.")
        table = self.query_one(DataTable)
        table.add_column("Stage?", width=7)
        table.add_column("Status", width=8)
        table.add_column("File Path")
        table.fixed_columns = 1 # Keep checkbox column fixed

        # Initial population
        self._update_file_status()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        button_id = event.button.id
        log.info(f"Button pressed: {button_id}")
        if button_id == "stage-selected-btn":
            self.action_stage_selected()
        elif button_id == "stage-all-btn":
            self.action_stage_all()
        elif button_id == "skip-btn":
            self.action_skip_staging()

    def action_stage_all(self) -> None:
        """Selects all checkboxes and stages the files."""
        log.info("Stage All action triggered.")
        # Check all checkboxes
        for checkbox in self._checkboxes.keys():
            checkbox.value = True
        # Trigger the stage selected action
        self.action_stage_selected()

    def action_stage_selected(self) -> None:
        """Stage the selected files and refresh the screen."""
        log.info("Stage Selected action triggered.")
        selected_files_to_stage = []
        selected_files_to_remove = []

        for checkbox, file_info in self._checkboxes.items():
            if checkbox.value: # Check if the checkbox is checked
                status = file_info['status'].strip()
                file_path = file_info['file']
                if status in ('M', '??', 'A'): # Modified, Untracked, or Added -> git add
                    selected_files_to_stage.append(file_path)
                elif status == 'D': # Deleted -> git rm (stages the deletion)
                    selected_files_to_remove.append(file_path)

        if not selected_files_to_stage and not selected_files_to_remove:
            log.warning("No files selected for staging.")
            self.app.notify("No files selected to stage.", severity="warning")
            return

        log.info(f"Attempting to stage: {selected_files_to_stage}")
        log.info(f"Attempting to remove (stage deletion): {selected_files_to_remove}")

        # Run the staging command
        # Consider running in a worker thread if it might block significantly,
        # but for typical staging, direct call might be acceptable.
        success, message = stage_files(selected_files_to_stage, selected_files_to_remove)

        if success:
            log.info(f"Staging successful: {message}")
            self.app.notify(f"Staging successful.", severity="information", timeout=3) # Shorter timeout
            # Refresh the screen state instead of dismissing
            self._update_file_status()
        else:
            log.error(f"Staging failed: {message}")
            self.app.notify(f"Staging failed: {message}", severity="error", timeout=10)
            # Optionally refresh even on failure to show current state
            self._update_file_status()

    def action_skip_staging(self) -> None:
        """Skip staging and proceed by dismissing the modal."""
        log.info("Skip Staging / Continue action triggered.")
        # The result here doesn't strictly matter as main.py re-checks counts
        self.dismiss((False, [])) # Indicate staging was skipped/finished by user

    def action_quit_app(self) -> None:
        """Quit the application."""
        log.info("Quit action triggered from StageFilesScreen.")
        self.app.quit()