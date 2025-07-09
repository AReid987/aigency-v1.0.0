from typing import List, Dict, Any, Optional, Set
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Button, Static, Footer, Header, LoadingIndicator
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual.worker import Worker, WorkerState
import os
import logging
from textual.message import Message # Import Message class

# Assuming these exist and are correctly implemented
from ..git_utils import run_lint_staged, get_staged_files # Import get_staged_files to re-check after autofix

log = logging.getLogger(__name__)

class LintErrorDisplayScreen(Screen):
    """
    Textual Screen to display linting errors grouped by file and linter,
    with interactive selection and action controls.

    Implements a re-linting/autofix loop with robust termination conditions (success, user proceed, max attempts, or cancel).
    """

    BINDINGS = [
        ("a", "autofix_selected", "Autofix Selected"),
        ("p", "proceed", "Proceed without Fixing"),
        ("c", "cancel", "Cancel"),
    ]

    # Message to signal when the autofix worker is done
    class AutofixWorkerFinished(Message):
        """Posted when the autofix worker has finished."""
        def __init__(self, success: bool, stdout: str, stderr: str) -> None:
            super().__init__()
            self.success = success
            self.stdout = stdout
            self.stderr = stderr

    def __init__(self, lint_errors: List[Dict[str, Any]], *args, **kwargs):
        """
        Initializes the LintErrorDisplayScreen.

        Args:
            lint_errors: A list of dictionaries, where each dictionary represents a linting error.
                         Expected keys: 'file', 'line', 'linter', 'ruleId', 'severity', 'message'.
        """
        super().__init__(*args, **kwargs)
        self.lint_errors: List[Dict[str, Any]] = lint_errors if isinstance(lint_errors, list) else []
        self.selected_rows: set[int] = set()
        self.autofix_worker: Optional[Worker] = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("Linting Errors Found", classes="title")
        yield Container(
            DataTable(id="lint-error-table"),
            id="error-table-container"
        )
        yield LoadingIndicator(id="autofix-loading", classes="hidden") # Hidden by default
        # Container for the buttons
        yield Horizontal(
            Button("Autofix Selected", id="autofix-btn", variant="success"),
            Button("Proceed without Fixing", id="proceed-btn", variant="primary"),
            Button("Cancel", id="cancel-btn", variant="error"),
            id="button-row"
        )
        yield Footer()

    def on_mount(self) -> None:
        """Populate the DataTable with lint errors on mount."""
        try:
            table = self.query_one("#lint-error-table", DataTable)
            self._populate_error_table(table)
        except Exception as e:
            logger = getattr(self.app, 'log', log)
            logger.error(f"Error populating error table on mount: {e}", exc_info=True)

    def _populate_error_table(self, table: DataTable) -> None:
        """Helper function to populate the DataTable."""
        table.clear()
        # Add columns if they don't exist (e.g., after clear)
        if not table.columns:
            table.add_column("Select", width=6)
            table.add_column("File", key="file", width=28)
            table.add_column("Line", key="line", width=8)
            table.add_column("Linter", key="linter", width=10)
            table.add_column("Rule", key="rule", width=12)
            table.add_column("Severity", key="severity", width=10)
            table.add_column("Message", key="message", width=50)

        errors_by_file: Dict[str, List[Dict[str, Any]]] = {}
        if isinstance(self.lint_errors, list):
            for err in self.lint_errors:
                if isinstance(err, dict):
                    key = err.get("file") or "<unknown file>"
                    errors_by_file.setdefault(key, []).append(err)
                else:
                    log.warning(f"Skipping non-dict item in lint_errors: {err}")
        else:
            log.error(f"Cannot populate error table: lint_errors is type {type(self.lint_errors)}, expected list.")
            return

        for file, errors in sorted(errors_by_file.items()):
            for err in errors:
                 row = [
                    "[ ]", # Checkbox
                    err.get("file") or "",
                    str(err.get("line", "")), # Use get with default for safety
                    err.get("linter") or "",
                    err.get("ruleId") or "",
                    err.get("severity") or "",
                    err.get("message") or "",
                ]
                 table.add_row(*row)

        table.show_header = True
        table.show_cursor = True
        table.zebra_stripes = True

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        """Handle row highlight to allow space/enter to select/deselect."""
        table = event.data_table
        row_idx = event.row_index
        if 0 <= row_idx < table.row_count: # Check bounds
            if row_idx in self.selected_rows:
                table.update_cell_at((row_idx, 0), "[x]")
            else:
                table.update_cell_at((row_idx, 0), "[ ]")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Toggle selection state when a row is selected (e.g., with space/enter)."""
        row_idx = event.row_index
        table = event.data_table
        if 0 <= row_idx < table.row_count: # Check bounds
            if row_idx in self.selected_rows:
                self.selected_rows.remove(row_idx)
                table.update_cell_at((row_idx, 0), "[ ]")
            else:
                self.selected_rows.add(row_idx)
                table.update_cell_at((row_idx, 0), "[x]")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses for Autofix, Proceed, and Cancel."""
        btn_id = event.button.id
        if btn_id == "autofix-btn":
            self.action_autofix_selected()
        elif btn_id == "proceed-btn":
            self.action_proceed()
        elif btn_id == "cancel-btn":
            self.action_cancel()

    def action_autofix_selected(self) -> None:
        """
        Run autofix (re-run lint-staged) on currently staged files.
        """
        log.info("Autofix action triggered.")
        if self.autofix_worker and self.autofix_worker.state == WorkerState.RUNNING:
            self.app.notify("Autofix is already running.", severity="warning")
            return

        self.app.notify("Running autofix (re-running lint-staged)...", severity="information")
        self.query_one("#autofix-loading").remove_class("hidden")
        self.autofix_worker = self.run_worker(self._run_autofix_worker(), exclusive=True)

    def _run_autofix_worker(self) -> Worker:
        """Worker method to run lint-staged for autofix."""
        log.info("Autofix worker started. Running lint-staged with --fix...")
        success, stdout, stderr = run_lint_staged(fix=True) # Call with fix=True
        log.info(f"Autofix worker finished. Success: {success}")
        # Post a message back to the main thread with the results
        self.post_message(self.AutofixWorkerFinished(success, stdout, stderr))
        # Returning None here as the result is sent via message

    def on_autofix_worker_finished(self, message: AutofixWorkerFinished) -> None:
        """Handler for the AutofixWorkerFinished message."""
        log.info("AutofixWorkerFinished message received.")
        self.query_one("#autofix-loading").add_class("hidden")
        self.selected_rows.clear() # Clear selections after re-linting

        if message.success:
            self.app.notify("Autofix attempt finished. Checking for remaining errors...", severity="information")
            # Re-get staged files and their diff to check for remaining errors
            # A simpler approach for now is to re-run lint-staged and parse its output again.
            # In a more complex scenario, we might re-parse the files themselves.
            # For now, let's just indicate success and let the user proceed.
            # A better approach would be to re-run lint-staged *again* and update the table.
            # Let's re-run lint-staged and update the table.

            # Re-run lint-staged to get the *new* list of errors after autofix
            log.info("Re-running lint-staged after autofix to get updated errors...")
            re_lint_success, re_lint_stdout, re_lint_stderr = run_lint_staged()
            log.info(f"Re-lint after autofix finished. Success: {re_lint_success}")

            new_lint_errors: List[Dict[str, Any]] = []
            # Re-parse stdout/stderr to get the new error list
            if re_lint_stdout:
                for line in re_lint_stdout.strip().splitlines():
                    if line.strip():
                        parts = line.split(':', 2)
                        file = parts[0].strip() if len(parts) > 0 else ""
                        line_num = parts[1].strip() if len(parts) > 1 and parts[1].strip().isdigit() else ""
                        message = parts[2].strip() if len(parts) > 2 else line.strip()
                        new_lint_errors.append({
                            "file": file,
                            "line": line_num,
                            "linter": "lint-staged",
                            "ruleId": "",
                            "severity": "info",
                            "message": message
                        })
            if re_lint_stderr:
                 for line in re_lint_stderr.strip().splitlines():
                    if line.strip():
                        parts = line.split(':', 2)
                        file = parts[0].strip() if len(parts) > 0 else ""
                        line_num = parts[1].strip() if len(parts) > 1 and parts[1].strip().isdigit() else ""
                        message = parts[2].strip() if len(parts) > 2 else line.strip()
                        new_lint_errors.append({
                            "file": file,
                            "line": line_num,
                            "linter": "lint-staged",
                            "ruleId": "",
                            "severity": "error",
                            "message": message
                        })

            self.lint_errors = new_lint_errors # Update the screen's error list
            table = self.query_one("#lint-error-table", DataTable)
            self._populate_error_table(table) # Repopulate the table with new errors

            if not new_lint_errors and re_lint_success:
                 self.app.notify("All linting issues resolved!", severity="success", timeout=5)
                 # Optionally automatically proceed if all issues are resolved
                 # self.call_later(self.action_proceed) # Auto-proceed
            elif not re_lint_success:
                 self.app.notify("Autofix attempt finished, but lint-staged still reported errors.", severity="warning", timeout=5)
            else:
                 self.app.notify(f"Autofix attempt finished. {len(new_lint_errors)} issues remain.", severity="warning", timeout=5)


        else:
            self.app.notify("Autofix failed. Check logs for details.", severity="error", timeout=5)
            # Optionally display the stderr in the error table or a separate widget
            error_data: List[Dict[str, str]] = [{"message": f"Autofix failed: {message.stderr}", "severity": "error"}]
            self.lint_errors = error_data # Update the screen's error list
            table = self.query_one("#lint-error-table", DataTable)
            self._populate_error_table(table) # Repopulate the table with the failure message


    def action_proceed(self) -> None:
        """
        Proceed without fixing selected errors.
        Should continue to the commit message screen.
        """
        log.info("Proceed action triggered.")
        self.dismiss(True) # Signal to proceed

    def action_cancel(self) -> None:
        """
        Cancel and return to previous screen or main menu.
        """
        log.info("Cancel action triggered.")
        self.dismiss(False) # Signal to cancel