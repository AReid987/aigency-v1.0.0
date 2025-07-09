#
# File: main_menu_temp.py
# Project: devlog-xprt
# Created Date: Th Apr 2025
# Author: <<author>>
# -----
# Last Modified: Thu Apr 10 2025
# Modified By: Antonio J. Reid
# -----
# Copyright (c) 2025 10xAigency
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button

class MainMenuScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Button("Generate Commit", id="generate-commit")
        yield Button("Configuration", id="configuration")
        yield Button("Pull Requests (Coming Soon)", disabled=True)
        yield Button("Issues (Coming Soon)", disabled=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "generate-commit":
            # TODO: Replace with actual commit generation screen logic
            from .commit_message_screen import CommitMessageScreen
            self.app.push_screen(CommitMessageScreen(ai_available=True))
        elif event.button.id == "configuration":
            from .configuration import ConfigurationScreen
            self.app.push_screen(ConfigurationScreen())

    def action_quit(self) -> None:
        self.app.exit()