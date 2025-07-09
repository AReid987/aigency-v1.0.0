#
 # File: commit_message_screen.py                                              #
 # Project: @xprt/xprt-commit                                                  #
 # Created Date: Su Apr 2025                                                   #
 # Author: <<author>                                                           #
 # -----                                                                       #
 # Last Modified: Tue Apr 15 2025                                              #
 # Modified By: Antonio J. Reid                                                #
 # -----                                                                       #
 # Copyright (c) 2025 10xAigency                                               #
 # -----                                                                       #
 # HISTORY:                                                                    #
 # Date      	By	Comments                                                   #
 # ----------	---	---------------------------------------------------------  #


import asyncio
import logging
from textual.screen import ModalScreen
from textual.widgets import Button, Static, Label, TextArea, Header, Footer
from textual.containers import Container
from textual.app import ComposeResult
from textual.message import Message
from typing import Optional, List, Dict, Any

# Assuming these exist and are correctly implemented
from ..ai_utils import call_ollama_commit_message
from ..git_utils import get_staged_diff # Import get_staged_diff if needed in this screen, although it's likely called in main.py before pushing this screen

log = logging.getLogger(__name__)

class StartAIWorker(Message):
    """Message to trigger the AI worker, carrying the diff content."""
    def __init__(self, diff_content: str):
        super().__init__()
        self.diff_content = diff_content

class CommitMessageScreen(ModalScreen[Optional[str]]):
    """
    A modal screen to generate and confirm the commit message.
    Returns the commit message string or None if cancelled.
    """
    def __init__(self, diff_content: str = "", ai_available: bool = True, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.diff_content = diff_content # Store diff content
        self.ai_available = ai_available
        self.commit_message: str = ""
        self.state = "choice" # 'choice', 'editing'
        self.status_message = ""
        self._current_diff_for_worker: str | None = None # This might not be needed if diff is passed directly to worker

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Lint: All checks passed. Ready to commit.", id="lint-success")
        if self.status_message:
            yield Static(self.status_message, id="status-msg")
        # Container for choice state
        with Container(id="choice-container") as choice_container:
            choice_container.styles.display = "block" if self.state == "choice" else "none"
            yield Label("How do you want to write your commit message?")
            yield Button("AI Suggestion", id="ai-btn", disabled=not self.ai_available)
            yield Button("Manual Entry", id="manual-btn")
            yield Button("Cancel", id="cancel-btn", variant="error") # Use variant for cancel

        # Container for editing state
        with Container(id="editing-container") as editing_container:
            editing_container.styles.display = "block" if self.state == "editing" else "none"
            yield Label("Edit your commit message below. Blank to cancel.")
            # Ensure the ID is correct and unique
            yield TextArea(self.commit_message, id="commit-message-area")
            yield Button("Confirm", id="confirm-btn", variant="success") # Use variant for confirm
            yield Button("Commit", id="commit-btn", variant="primary") # New Commit button
            yield Button("Cancel", id="cancel-btn", variant="error") # Use variant for cancel
        yield Footer()

    def on_mount(self) -> None:
        """Set initial focus based on state."""
        self._set_initial_focus()

    def _set_initial_focus(self) -> None:
        """Helper to set focus based on current state."""
        try:
            if self.state == "choice":
                btn = self.query_one("#ai-btn", Button)
                if not btn.disabled:
                    self.set_focus(btn)
                else:
                    self.set_focus(self.query_one("#manual-btn", Button))
            elif self.state == "editing":
                 # Use call_later to ensure the widget exists after compose
                 self.call_later(self.focus_text_area)
        # Catch general exceptions during focus setting
        except Exception as e:
            self.app.log.warning(f"Could not set initial focus: {e}", exc_info=True)


    def focus_text_area(self) -> None:
        """Safely focuses the commit message text area."""
        try:
            text_area = self.query_one("#commit-message-area", TextArea)
            text_area.focus()
            self.app.log.info("Focused #commit-message-area")
        # Catch general exceptions during focus setting
        except Exception as e:
            self.app.log.error(f"Error focusing text area: {e}", exc_info=True)


    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        self.app.log.info(f"Button pressed: {button_id}")
        self.status_message = f"Processing: {button_id}" # Restored
        self.refresh() # Refresh status message immediately - Restored

        # Debugging lines removed

        if button_id == "ai-btn":
            # Restore UI updates and post message instead of calling worker directly
            self.status_message = "Generating AI commit message (please wait)..."
            self.refresh()
            self.app.log.info("Posting StartAIWorker message with diff content.")
            # Pass the diff_content stored in the instance variable
            self.post_message(StartAIWorker(diff_content=self.diff_content))
            self.app.log.info("StartAIWorker message posted.")
        elif button_id == "manual-btn":
            self.state = "editing"
            self.commit_message = "" # Start with empty for manual entry
            # Update container visibility
            try:
                choice_container = self.query_one("#choice-container", Container)
                editing_container = self.query_one("#editing-container", Container)
                choice_container.styles.display = "none"
                editing_container.styles.display = "block"
                # Update TextArea content explicitly if needed (already empty here)
                # text_area = self.query_one("#commit-message-area", TextArea)
                # text_area.text = self.commit_message
            except Exception as e:
                self.app.log.error(f"Error switching to edit view: {e}", exc_info=True)
            # Focus is handled by call_later after UI update
            self.call_later(self.focus_text_area)
        elif button_id == "cancel-btn":
            self.app.log.info("Cancel button pressed, dismissing screen with None.")
            self.dismiss(None) # Dismiss with None to indicate cancellation
        elif button_id == "confirm-btn":
            self.app.log.info("Confirm button pressed.")
            try:
                text_area = self.query_one("#commit-message-area", TextArea)
                self.commit_message = text_area.text.strip()
                if self.commit_message:
                    self.app.log.info(f"Commit message confirmed (length: {len(self.commit_message)}), dismissing screen.")
                    self.dismiss(self.commit_message) # Dismiss with the commit message
                else:
                    self.app.log.warning("Commit message is empty, cannot confirm. Dismissing with None.")
                    self.status_message = "Commit message cannot be empty. Cancelling."
                    self.refresh() # Keep refresh here as it's needed for user feedback
                    self.set_timer(1.5, lambda: self.dismiss(None)) # Dismiss with None after a short delay
            # Correctly placed except block for the try starting on line 131
            except Exception as e:
                 self.app.log.error(f"Error during confirm: {e}", exc_info=True)
                 self.status_message = f"Error: {e}"
                 self.refresh() # Refresh needed here too
                 self.dismiss(None) # Dismiss with None on error


    # New message handler method (correctly indented)
    async def on_start_aiworker(self, message: StartAIWorker) -> None: # Renamed and made async
        """Handles the message to start the AI worker."""
        self.app.log.info("StartAIWorker message received.")
        self.app.log.info(f"Received diff_content (length: {len(message.diff_content)} chars).")
        # Store diff content in instance variable before starting worker - This might not be needed now
        self._current_diff_for_worker = message.diff_content # Keep for now, but consider removing later

        self.app.log.info("Attempting to call self.run_worker...")
        # Call run_worker, passing the diff_content as an argument to the worker function
        # The worker function signature must match the arguments passed here.
        self.run_worker(self.generate_ai_commit_message_worker, message.diff_content, exclusive=True, thread=True)
        self.app.log.info("Call to self.run_worker completed from message handler.")


    # Following method (correctly indented)
    async def generate_ai_commit_message_worker(self, diff_content: str): # Added diff_content argument
        """Worker to generate commit message using AI based on provided diff (runs async)."""
        # Use standard logging within the worker
        log = logging.getLogger(__name__) # Get logger instance
        log.info("AI Worker started.") # Use standard logger
        ai_msg = "[AI suggestion failed]" # Default message

        # No longer retrieve from instance variable if diff is passed directly, but keeping the check for safety
        # diff_content = self._current_diff_for_worker # Remove this line if passing directly
        # Remove clearing the temporary storage
        # self._current_diff_for_worker = None # Remove this line

        if diff_content is None: # Keep this check, although diff_content should always be a string now
            log.error("AI Worker: diff_content was None. Cannot proceed.")
            ai_msg = "[Error: Diff content not provided to worker]" # Updated error message
            # Skip the rest of the processing if diff is None
        else:
            # Original logic using the diff_content argument
            call_ollama_commit_message = None
            try:
                # Attempt imports first
                from ..ai_utils import call_ollama_commit_message # Import the correct function
                log.info("AI Worker: Imports successful.")

                try:
                    log.info(f"AI Worker: Using diff content length: {len(diff_content)}")

                    if diff_content.strip(): # Check if diff is not empty
                         log.info("AI Worker: Calling Ollama for commit message...")
                         ai_msg = await asyncio.to_thread(call_ollama_commit_message, diff_content) or ai_msg
                         log.info(f"AI Worker: Ollama commit message call complete. Message: '{ai_msg}'")
                    else:
                         ai_msg = "[No diff content provided to AI worker]"
                         log.warning("AI Worker: Diff content was empty.")

                except Exception as e_inner: # Inner exception during ollama call
                    log.error(f"Error during AI processing (Ollama call): {e_inner}", exc_info=True)
                    if ai_msg == "[AI suggestion failed]":
                        ai_msg = f"[Error during AI generation: Check logs]"

            except ImportError as ie: # Outer exception for imports
                log.error(f"ImportError in AI worker: {ie}", exc_info=True)
                ai_msg = f"[Error importing dependencies: Check logs]"
            except Exception as e_outer: # Catch any other unexpected error
                log.error(f"Unexpected error in AI worker: {e_outer}", exc_info=True)
                if ai_msg == "[AI suggestion failed]":
                     ai_msg = f"[Unexpected error in worker: Check logs]"

        # This log now happens regardless of import success/failure
        log.info("AI Worker: Preparing UI update.")
        # Note: The UI update part still uses self.app.log implicitly via call_from_thread and within update_ui
        if ai_msg == "[Ollama] Model 'gemma3' not found. Please run 'ollama pull gemma3'.":
            self.status_message = "Ollama model 'gemma3' not found. Please run 'ollama pull gemma3' in your terminal and try again."
            self.commit_message = "Ollama model 'gemma3' not found. Please run 'ollama pull gemma3' in your terminal and try again."
        def update_ui():
            # This part runs in the main thread via call_from_thread, so self.app.log *should* work here
            self.app.log.info("AI Worker: update_ui called.") # Use self.app.log here

            if ai_msg == "[Ollama] Model 'gemma3' not found. Please run 'ollama pull gemma3'.":
                self.status_message = "Ollama model 'gemma3' not found. Please run 'ollama pull gemma3' in your terminal and try again."
                self.commit_message = "Ollama model 'gemma3' not found. Please run 'ollama pull gemma3' in your terminal and try again."
            else:
                self.status_message = "AI processing complete. Edit or confirm."
                self.commit_message = ai_msg
            # Update status message first
            try:
                status_widget = self.query_one("#status-msg", Static)
                # Check if status widget exists before updating
                if status_widget:
                    status_widget.update(self.status_message)
                else:
                    self.app.log.warning("Could not find #status-msg widget to update.") # Use self.app.log here
            except Exception as e:
                 self.app.log.error(f"Error updating status message: {e}", exc_info=True) # Use self.app.log here


            self.state = "editing"

            # Update container visibility
            try:
                choice_container = self.query_one("#choice-container", Container)
                editing_container = self.query_one("#editing-container", Container)
                choice_container.styles.display = "none"
                editing_container.styles.display = "block"
                # Update TextArea content explicitly AFTER container is visible
                text_area = self.query_one("#commit-message-area", TextArea)
                text_area.load_text(self.commit_message) # Use load_text for robustness
            except Exception as e:
                self.app.log.error(f"Error updating UI for AI message: {e}", exc_info=True) # Use self.app.log here

            # Use call_later to focus after the UI update
            self.call_later(self.focus_text_area)
            self.app.log.info("AI Worker: update_ui finished.") # Use self.app.log here

        # Schedule UI update in the main thread
        log.info("AI Worker: Scheduling UI update via call_from_thread.") # Use standard logger
        self.app.call_from_thread(update_ui)
        log.info("AI Worker finished.") # Use standard logger