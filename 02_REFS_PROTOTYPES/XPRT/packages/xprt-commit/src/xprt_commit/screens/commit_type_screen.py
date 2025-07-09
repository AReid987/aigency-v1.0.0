#
# File: commit_type_screen.py                                                 #
# Project: xprt-commit                                                        #
# Created Date: Fr Apr 2025                                                   #
# Author: <<author>                                                           #
# -----                                                                       #
# Last Modified: Fri Apr 11 2025                                              #
# Modified By: Antonio J. Reid                                                #
# -----                                                                       #
# Copyright (c) 2025 10xAigency                                               #
# -----                                                                       #
# HISTORY:                                                                    #
# Date      	By	Comments                                                   #
# ----------	---	---------------------------------------------------------  #


# Filename: packages/xprt-commit/src/xprt_commit/screens/commit_type_screen.py
# Path: packages/xprt-commit/src/xprt_commit/screens
"""
Commit Type Selection Screen for xprt-commit.

This screen will allow the user to select the type of commit
(e.g., feat, fix, chore, etc.).
"""

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Header, Footer, Label, RadioSet, RadioButton, Button
from textual.on import on

# Commit types based on commitlint.config.js type-enum
COMMIT_TYPES = [
    'feat', 'fix', 'docs', 'style', 'refactor', 'perf', 'test',
    'build', 'ci', 'chore', 'revert'
]

class CommitTypeScreen(Screen):
    """Screen for selecting the commit type."""

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("esc", "app.pop_screen", "Back"),
    ]

    def __init__(self, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.selected_type: str | None = None

    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield Header()
        yield Label("Select Commit Type:", classes="label")
        with VerticalScroll():
            with RadioSet(id="commit_type_radioset") as radio_set:
                for commit_type in COMMIT_TYPES:
                    yield RadioButton(commit_type, id=f"type-{commit_type}")
        yield Button("OK", id="ok_button", variant="primary", disabled=True) # Disable initially
        yield Footer()

    @on(RadioSet.Changed)
    def enable_button(self, event: RadioSet.Changed) -> None:
        """Enable the OK button when a selection is made."""
        self.selected_type = event.pressed.label.plain # Store the selected type string
        self.query_one("#ok_button", Button).disabled = False
        # Optional: Log the selection as it happens
        # self.app.log(f"Selected commit type: {self.selected_type}")

    @on(Button.Pressed, "#ok_button")
    def confirm_selection(self) -> None:
        """Handle the OK button press."""
        if self.selected_type:
            self.app.log(f"Confirmed commit type: {self.selected_type}")
            # TODO: Pass the selected type back or store it for the next step
            self.app.pop_screen()
        else:
            self.app.log("No commit type selected.") # Should not happen if button is disabled

    def action_quit(self) -> None:
        """Action to quit the application."""
        self.app.exit()