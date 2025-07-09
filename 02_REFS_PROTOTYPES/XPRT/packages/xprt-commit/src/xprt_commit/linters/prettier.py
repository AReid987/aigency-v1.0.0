#
# File: prettier.py
# Project: @xprt/xprt-commit
# Created Date: Fri Apr 12 2025
# Author: Roo
# -----
# Last Modified: Fri Apr 12 2025
# Modified By: Roo
# -----
# Copyright (c) 2025 10xAigency
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
# 2025-04-12    Roo Initial implementation based on XPRTC-TASK-010.

import subprocess
from typing import List, Dict, Any, Optional

def run_prettier_check(staged_files: List[str]) -> Dict[str, Any]:
    """
    Runs Prettier on the provided files and checks for formatting differences.

    Args:
        staged_files (List[str]): List of file paths to check.

    Returns:
        Dict[str, Any]: {
            'needs_formatting': bool,  # Indicates if any files need formatting.
            'files': Optional[List[str]],  # List of files needing formatting, if any.
            'stdout': str,    # Raw stdout from the prettier process.
            'stderr': str,    # Raw stderr from the prettier process.
            'error': Optional[str] # Description of operational errors (e.g., command not found).
        }
    """
    result: Dict[str, Any] = {
        'needs_formatting': False,
        'files': None,
        'stdout': '',
        'stderr': '',
        'error': None,
    }

    if not staged_files:
        result['error'] = 'No files provided to run Prettier.'
        return result

    cmd = ['prettier', '--check'] + staged_files

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,  # Handle exit codes manually
            encoding='utf-8'
        )
        result['stdout'] = proc.stdout
        result['stderr'] = proc.stderr

        if proc.returncode == 0:
            # Prettier ran successfully and found no formatting issues.
            result['needs_formatting'] = False
        elif proc.returncode == 1:
            # Prettier found formatting issues.
            result['needs_formatting'] = True
            # Parse the output to extract the files needing formatting, if possible
            files_needing_format = []
            for line in proc.stderr.splitlines():
                if "would reformat" in line:
                    parts = line.split(" ")
                    if len(parts) > 1:
                        files_needing_format.append(parts[-1])
            if files_needing_format:
                result['files'] = files_needing_format
        else:
            # Prettier failed due to an actual error.
            result['error'] = (
                f'Prettier failed with exit code {proc.returncode}.\n'
                f'Stderr:\n{proc.stderr}\n'
                f'Stdout:\n{proc.stdout}'
            )
    except FileNotFoundError:
        result['error'] = 'Prettier command not found. Please ensure Prettier is installed and accessible in your PATH.'
    except Exception as e:
        result['error'] = f'An unexpected error occurred while running Prettier: {str(e)}'

    return result