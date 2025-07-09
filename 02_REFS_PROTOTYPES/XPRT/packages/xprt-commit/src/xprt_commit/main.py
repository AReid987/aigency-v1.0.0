# Filename: /Users/antonioreid/01_DOING/XPRT/packages/xprt-commit/src/xprt_commit/main.py
# Path: /Users/antonioreid/01_DOING/XPRT/packages/xprt-commit/src/xprt_commit
# Created Date: Thursday, April 10th 2025, 11:19:00 pm
# Author: Antonio J. Reid
#
# Copyright (c) 2025 10xAigency

import logging

# Configure logging to write to a file
logging.basicConfig(level=logging.INFO, filename='tui_debug.log', format='%(asctime)s - %(levelname)s - %(message)s')

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.binding import Binding

# Import screens
from .screens.main_menu import MainMenuScreen
from .screens.configuration import ConfigurationScreen
from .screens.pull_requests import PullRequestsScreen
from .screens.issues import IssuesScreen # noqa: F401
from .screens.commit_message_screen import CommitMessageScreen # Import needed for message posting
from .screens.error_display import LintErrorDisplayScreen
from .screens.stage_files_screen import StageFilesScreen
# Ensure all necessary functions are imported
from .git_utils import get_staged_files, get_unstaged_files, stage_files, run_lint_staged, get_staged_diff, commit_staged_files
from typing import List, Tuple, Dict, Any


class XprtCommitApp(App):
    """A Textual app to manage commits."""

    CSS_PATH = "main.tcss" # Assuming a CSS file exists or will be created
    BINDINGS = [
        Binding(key="d", action="toggle_dark", description="Toggle dark mode"),
        Binding(key="g", action="generate_commit", description="Generate Commit"), # Placeholder action
        Binding(key="c", action="show_config", description="Configuration"),
        Binding(key="p", action="show_pull_requests", description="Pull Requests"),
        Binding(key="i", action="show_issues", description="Issues"),
        Binding(key="m", action="show_main_menu", description="Main Menu"), # Added binding to return to main menu
        Binding(key="q", action="quit", description="Quit"),
    ]

    # Add a variable to store the commit message result
    commit_message: str | None = None

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        # Start with the main menu screen
        self.log.info("App mounted, pushing MainMenuScreen.")
        self.push_screen(MainMenuScreen())

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark
        self.log.info(f"Dark mode toggled: {self.dark}")

    def action_show_main_menu(self) -> None:
        """Action to show the main menu screen."""
        self.log.info("Action show_main_menu triggered.")
        # Check if the current screen is already MainMenuScreen to avoid duplicates
        if not isinstance(self.screen, MainMenuScreen):
             # Simple approach: just push it. More complex might involve checking stack.
             self.log.info("Pushing MainMenuScreen.")
             self.push_screen(MainMenuScreen())
        else:
             self.log.info("Already on MainMenuScreen.")


    def action_show_config(self) -> None:
        """Action to show the configuration screen."""
        self.log.info("Action show_config triggered.")
        if not isinstance(self.screen, ConfigurationScreen):
            self.log.info("Pushing ConfigurationScreen.")
            self.push_screen(ConfigurationScreen())
        else:
            self.log.info("Already on ConfigurationScreen.")

    def action_show_pull_requests(self) -> None:
        """Action to show the pull requests screen."""
        self.log.info("Action show_pull_requests triggered.")
        if not isinstance(self.screen, PullRequestsScreen):
            self.log.info("Pushing PullRequestsScreen.")
            self.push_screen(PullRequestsScreen())
        else:
             self.log.info("Already on PullRequestsScreen.")

    def action_show_issues(self) -> None:
        """Action to show the issues screen."""
        self.log.info("Action show_issues triggered.")
        if not isinstance(self.screen, IssuesScreen):
            self.log.info("Pushing IssuesScreen.")
            self.push_screen(IssuesScreen())
        else:
            self.log.info("Already on IssuesScreen.")

    def action_generate_commit(self) -> None:
        """Start the lint+commit flow."""
        self.log.info("Action generate_commit triggered.")
        # Schedule the async method to run after current event handling
        self.call_later(self.start_commit_flow)

    async def start_commit_flow(self) -> None:
        """Check for staged/unstaged files, optionally stage, then proceed to lint and commit."""
        self.log.info("Starting commit flow check (async)...")
        try:
            self.log.info("Checking for staged and unstaged files...")
            staged = get_staged_files()
            unstaged = get_unstaged_files()
            staged_count = len(staged)
            unstaged_count = len(unstaged)
            self.log.info(f"Initial check: {staged_count} staged, {unstaged_count} unstaged.")
            self.app.notify(f"Found {staged_count} staged file(s).", severity="information")

            if unstaged:
                self.log.info("Unstaged files found. Pushing StageFilesScreen.")
                self.app.notify(f"Found {unstaged_count} unstaged file(s). Opening staging screen...", severity="information")
                # Define the callback to handle the result from StageFilesScreen
                def staging_callback(result: Tuple[bool, List[str]]):
                    # Use call_later to ensure the callback runs in the main event loop thread
                    # Pass the result to _handle_staging_result
                    self.call_later(self._handle_staging_result, result)

                self.push_screen(StageFilesScreen(unstaged_files=unstaged), staging_callback)
            elif not staged:
                # No unstaged files AND no staged files
                self.log.warning("No staged or unstaged files found. Nothing to commit.")
                self.app.notify("No changes detected (staged or unstaged). Nothing to commit.", severity="warning", timeout=6)
            else:
                # No unstaged files, but staged files exist
                self.log.info("No unstaged files found, but staged files exist. Proceeding directly to lint.")
                # Use call_later to schedule the next step
                # Pass dummy result to _handle_staging_result which then calls _proceed_to_lint_and_commit
                self.call_later(self._proceed_to_lint_and_commit, (False, [])) # Indicate staging wasn't attempted

        except Exception as e:
            self.log.error(f"Error during initial commit flow check: {e}", exc_info=True)
            # Assuming get_staged_files/get_unstaged_files return strings starting with [ERROR: on failure]
            error_messages = []
            if isinstance(staged, list) and staged and staged[0].startswith("[ERROR:"):
                 error_messages.append(staged[0])
            if isinstance(unstaged, list) and unstaged and unstaged[0].startswith("[ERROR:"):
                 error_messages.append(unstaged[0])
            if not error_messages:
                 error_messages.append(f"An unexpected error occurred: {e}")

            error_data: List[Dict[str, str]] = [{"message": msg, "severity": "error"} for msg in error_messages]
            self.push_screen(LintErrorDisplayScreen(lint_errors=error_data)) # type: ignore


    async def _handle_staging_result(self, result: Tuple[bool, List[str]]) -> None:
        """Callback function after StageFilesScreen is dismissed."""
        staging_attempted, files_involved = result
        self.log.info(f"Staging screen dismissed. Attempted: {staging_attempted}, Files involved: {files_involved}")

        # Re-check staged files after potential staging
        final_staged = get_staged_files()
        final_staged_count = len(final_staged)
        self.log.info(f"After staging screen: {final_staged_count} file(s) are staged.")
        self.app.notify(f"Now {final_staged_count} file(s) are staged.", severity="information")

        if final_staged_count == 0:
             self.log.warning("No files staged after interaction. Nothing to commit.")
             self.app.notify("No changes are staged. Nothing to commit.", severity="warning", timeout=6)
             return # Stop the flow

        # Proceed to linting only if there are staged files
        await self._proceed_to_lint_and_commit() # Directly await the async method

    async def _proceed_to_lint_and_commit(self) -> None:
        """Run lint-staged, display results, handle autofix, get final diff, then prompt for commit message."""
        self.log.info("Proceeding to lint-staged...")
        # Check again if there are staged files before running lint-staged.
        staged_files_before_lint = get_staged_files()
        if not staged_files_before_lint:
            self.log.warning("Proceed to lint called, but no files are staged. Aborting.")
            self.app.notify("No changes are staged. Nothing to commit.", severity="warning", timeout=6)
            return

        try:
            # Step 1: Run lint-staged
            self.log.info("Running lint-staged...")
            lint_success, lint_stdout, lint_stderr = run_lint_staged()
            self.log.info(f"lint-staged completed. Success: {lint_success}")
            self.log.debug(f"lint-staged stdout:\n{lint_stdout}")
            self.log.debug(f"lint-staged stderr:\n{lint_stderr}")

            # Prepare lint errors for display
            lint_errors_to_display: List[Dict[str, Any]] = []

            # Simple approach: Treat each line of stderr/stdout as a message for now
            # TODO: Implement proper parsing of linter output (e.g., JSON format from linters)
            if lint_stdout:
                for line in lint_stdout.strip().splitlines():
                    if line.strip():
                         # Attempt basic parsing for common linter output formats (e.g., file:line: message)
                         parts = line.split(':', 2)
                         file = parts[0].strip() if len(parts) > 0 else ""
                         line_num = parts[1].strip() if len(parts) > 1 and parts[1].strip().isdigit() else ""
                         message = parts[2].strip() if len(parts) > 2 else line.strip()
                         lint_errors_to_display.append({
                             "file": file,
                             "line": line_num,
                             "linter": "lint-staged", # Generic linter name for now
                             "ruleId": "", # Cannot determine rule ID from simple parsing
                             "severity": "info", # Default to info, could try to infer from message
                             "message": message
                         })

            if lint_stderr:
                for line in lint_stderr.strip().splitlines():
                    if line.strip():
                         # Attempt basic parsing for common linter output formats
                         parts = line.split(':', 2)
                         file = parts[0].strip() if len(parts) > 0 else ""
                         line_num = parts[1].strip() if len(parts) > 1 and parts[1].strip().isdigit() else ""
                         message = parts[2].strip() if len(parts) > 2 else line.strip()
                         lint_errors_to_display.append({
                             "file": file,
                             "line": line_num,
                             "linter": "lint-staged", # Generic linter name for now
                             "ruleId": "",
                             "severity": "error", # Assume stderr indicates error/warning
                             "message": message
                         })

            if lint_errors_to_display:
                self.log.info(f"Pushing LintErrorDisplayScreen with {len(lint_errors_to_display)} errors/warnings.")
                # Define the callback to handle the result from LintErrorDisplayScreen
                def lint_screen_callback(proceed: bool):
                    # Use call_later to ensure the callback runs in the main event loop thread
                    self.call_later(self._handle_lint_screen_result, proceed)

                self.push_screen(LintErrorDisplayScreen(lint_errors=lint_errors_to_display), lint_screen_callback) # type: ignore
            elif not lint_success:
                 # No structured errors found, but lint-staged reported failure
                 self.log.error("lint-staged failed with no parseable errors. Halting commit process.")
                 error_data: List[Dict[str, str]] = [{"message": "Lint-staged failed with unparseable output. Please check logs for details.", "severity": "error"}]
                 self.push_screen(LintErrorDisplayScreen(lint_errors=error_data)) # type: ignore
            else:
                # lint-staged succeeded and had no output (or only uninteresting output)
                self.log.info("lint-staged succeeded with no significant output. Proceeding to commit message generation.")
                # Proceed to getting the diff and generating the message
                await self._proceed_to_commit_message_generation()


        except FileNotFoundError:
            self.log.error("'npx' command not found. Make sure Node.js and npm/npx installed and in PATH.", exc_info=True)
            error_data: List[Dict[str, str]] = [{"message": "'npx' command not found. Make sure Node.js is installed.", "severity": "error"}]
            self.push_screen(LintErrorDisplayScreen(lint_errors=error_data)) # type: ignore
        except Exception as e:
            self.log.error(f"An unexpected error occurred during linting: {e}", exc_info=True)
            error_data: List[Dict[str, str]] = [{"message": f"An unexpected error occurred during linting: {e}. Check logs.", "severity": "error"}]
            self.push_screen(LintErrorDisplayScreen(lint_errors=error_data)) # type: ignore


    async def _handle_lint_screen_result(self, proceed: bool) -> None:
        """Callback function after LintErrorDisplayScreen is dismissed."""
        self.log.info(f"LintErrorDisplayScreen dismissed. Proceed: {proceed}")
        if proceed:
            # Re-check staged files after potential autofixing
            staged_files_after_lint_screen = get_staged_files()
            if not staged_files_after_lint_screen:
                 self.log.warning("No files staged after lint screen interaction. Aborting commit.")
                 self.app.notify("No changes are staged after linting/fixing. Nothing to commit.", severity="warning", timeout=6)
                 return

            self.log.info("User chose to proceed after linting. Proceeding to commit message generation.")
            await self._proceed_to_commit_message_generation()
        else:
            self.log.info("User chose to cancel after linting. Aborting commit.")
            self.app.notify("Commit process cancelled.", severity="information", timeout=3)
            # Optionally navigate back to main menu or previous screen
            # self.push_screen(MainMenuScreen())


    async def _proceed_to_commit_message_generation(self) -> None:
        """Get final diff and push the CommitMessageScreen."""
        self.log.info("Getting final staged diff for commit message generation...")
        final_diff = get_staged_diff()
        self.log.info(f"Final staged diff obtained (length: {len(final_diff)} chars).")
        self.log.info(f"Final diff content before pushing CommitMessageScreen: {final_diff!r}")

        if final_diff.startswith("[ERROR:"):
            self.log.error(f"Failed to get final staged diff: {final_diff}")
            error_data: List[Dict[str, str]] = [{"message": f"Error getting final diff: {final_diff}. Check logs.", "severity": "error"}]
            self.push_screen(LintErrorDisplayScreen(lint_errors=error_data)) # type: ignore
            return

        if not final_diff.strip():
            self.log.warning("No changes staged after lint-staged. Cannot generate commit message.")
            self.app.notify("No changes are staged after linting/fixing. Cannot generate commit message.", severity="warning", timeout=6)
            return

        self.log.info("Final diff obtained. Instantiating and pushing CommitMessageScreen.")
        # Instantiate CommitMessageScreen and pass the final_diff as diff_content
        commit_message_screen = CommitMessageScreen(diff_content=final_diff)
        self.push_screen(commit_message_screen)
        self.log.info("CommitMessageScreen pushed with final diff.")

    async def _proceed_to_commit_message_generation(self) -> None:
        """Get the final staged diff and prompt for commit message."""
        self.log.info("Proceeding to commit message generation...")
        # Step 2: Get the FINAL staged diff after lint-staged potentially modified files
        self.log.info("Getting final staged diff...")
        final_diff = get_staged_diff()
        self.log.info(f"Final staged diff obtained (length: {len(final_diff)} chars).")
        self.log.debug(f"Final diff content before posting message: {final_diff!r}")

        if final_diff.startswith("[ERROR:"):
            self.log.error(f"Failed to get final staged diff: {final_diff}")
            error_data: List[Dict[str, str]] = [{"message": f"Error getting final diff: {final_diff}. Check logs.", "severity": "error"}]
            self.push_screen(LintErrorDisplayScreen(lint_errors=error_data)) # type: ignore
            return

        if not final_diff.strip():
            self.log.warning("No changes staged after lint-staged and potential autofix.")
            self.app.notify("No changes are staged after linting/fixing. Nothing to commit.", severity="warning", timeout=6)
            return

        # Step 3: Prompt for commit message using the CommitMessageScreen
        self.log.info("Pushing CommitMessageScreen to get commit message.")

        def commit_message_callback(commit_message: str | None) -> None:
            """Callback function after CommitMessageScreen is dismissed."""
            self.log.info(f"CommitMessageScreen dismissed. Message received: {commit_message is not None}")
            if commit_message is not None:
                self.log.info(f"Commit message provided (length: {len(commit_message)}). Proceeding to execute commit.")
                self.call_later(self._execute_final_commit, commit_message) # Schedule the final commit
            else:
                self.log.info("Commit message generation cancelled by user. Aborting commit.")
                self.app.notify("Commit message cancelled. Aborting.", severity="information", timeout=3)
                # Optionally navigate back to main menu or previous screen
                # self.push_screen(MainMenuScreen())


        # Push the CommitMessageScreen, passing the diff content and the callback
        # We need to pass the diff content to the CommitMessageScreen so it can generate the AI message.
        # The CommitMessageScreen will handle the AI worker internally.
        self.push_screen(CommitMessageScreen(ai_available=True), commit_message_callback) # Assuming AI is available
        self.log.info("CommitMessageScreen pushed.")

    async def _execute_final_commit(self, message: str) -> None:
        """Execute the final git commit command."""
        self.log.info("Executing final git commit...")
        # Assuming commit_staged_changes is implemented in git_utils.py
        success, output = commit_staged_files(message)

        if success:
            self.log.info("Final commit successful.")
            self.app.notify("Commit successful!", severity="information", timeout=5)
            # Optionally navigate back to main menu or close the app
            # self.push_screen(MainMenuScreen())
        else:
            self.log.error(f"Final commit failed: {output}")
            error_data: List[Dict[str, str]] = [{"message": f"Commit failed: {output}", "severity": "error"}]
            self.push_screen(LintErrorDisplayScreen(lint_errors=error_data)) # Reuse error screen for commit errors


    def action_quit(self) -> None:
        """Action to quit the application."""
        self.log.info("Quit action triggered.")
        self.exit()


if __name__ == "__main__":
    app = XprtCommitApp()
    # Use run() which handles the event loop
    app.run()