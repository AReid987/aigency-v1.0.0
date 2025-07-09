#
 # File: pull_requests.py                                                      #
 # Project: devlog-xprt                                                        #
 # Created Date: Th Apr 2025                                                   #
 # Author: <<author>                                                           #
 # -----                                                                       #
 # Last Modified: Thu Apr 10 2025                                              #
 # Modified By: Antonio J. Reid                                                #
 # -----                                                                       #
 # Copyright (c) 2025 10xAigency                                               #
 # -----                                                                       #
 # HISTORY:                                                                    #
 # Date      	By	Comments                                                   #
 # ----------	---	---------------------------------------------------------  #




from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label


class PullRequestsScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Label("Pull Requests Screen", id="pull-requests-label")