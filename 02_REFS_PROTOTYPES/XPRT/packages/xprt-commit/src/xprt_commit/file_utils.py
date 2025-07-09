#
 # File: file_utils.py                                                         #
 # Project: @xprt/xprt-commit                                                  #
 # Created Date: Sa Apr 2025                                                   #
 # Author: <<author>                                                           #
 # -----                                                                       #
 # Last Modified: Sat Apr 12 2025                                              #
 # Modified By: Antonio J. Reid                                                #
 # -----                                                                       #
 # Copyright (c) 2025 10xAigency                                               #
 # -----                                                                       #
 # HISTORY:                                                                    #
 # Date      	By	Comments                                                   #
 # ----------	---	---------------------------------------------------------  #




"""
file_utils.py

Utilities for applying code patches (diffs) or replacing file content.

Author: Roo
Created: 2025-04-12
"""

from typing import Optional
import difflib
import os

def apply_unified_diff(file_path: str, diff_text: str) -> bool:
    """
    Applies a unified diff to the given file.

    Args:
        file_path (str): Path to the file to patch.
        diff_text (str): Unified diff as a string.

    Returns:
        bool: True on success, False on failure.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            original_lines = f.readlines()

        diff_lines = diff_text.splitlines(keepends=True)
        patched = list(difflib.restore(diff_lines, 2))  # 2 = apply "after" version

        if not patched:
            return False

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(patched)
        return True
    except Exception as e:
        # Optionally log error
        return False

def replace_file(file_path: str, new_content: str) -> bool:
    """
    Replaces the entire content of the given file.

    Args:
        file_path (str): Path to the file.
        new_content (str): New file content.

    Returns:
        bool: True on success, False on failure.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    except Exception as e:
        # Optionally log error
        return False