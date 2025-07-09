#
 # File: biome.py                                                              #
 # Project: @xprt/xprt-commit                                                  #
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




# File: biome.py
# Project: xprt-commit
# Created Date: Fri Apr 11 2025
# Author: Antonio J. Reid
# -----
# Copyright (c) 2025 10xAigency
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------

import subprocess
import json
from typing import List, Union, Any, Dict, Optional

def run_biome(file_paths: List[str]) -> Union[List[Any], Dict[str, Any]]:
    """
    Run Biome.js linter on the given files using npx, capturing and parsing JSON output.

    Args:
        file_paths (List[str]): List of file paths to lint.

    Returns:
        Union[List[Any], Dict[str, Any]]: Parsed Biome JSON output on success,
        or a dictionary with error information on failure.
    """
    if not file_paths:
        return {"error": "No file paths provided."}

    # Build the Biome command
    command = ["npx", "biome", "check", "--formatter=json"] + file_paths

    try:
        proc = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False  # Don't raise on non-zero exit
        )
    except FileNotFoundError as e:
        return {"error": "npx or biome not found in PATH.", "exception": str(e)}
    except Exception as e:
        return {"error": "Failed to execute Biome.", "exception": str(e)}

    stdout = proc.stdout
    stderr = proc.stderr
    exit_code = proc.returncode

    if not stdout.strip():
        return {
            "error": "No output from Biome.",
            "stderr": stderr,
            "exit_code": exit_code
        }

    try:
        result = json.loads(stdout)
        return result
    except json.JSONDecodeError as e:
        return {
            "error": "Failed to parse Biome JSON output.",
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": exit_code,
            "exception": str(e)
        }

    # Fallback: should not reach here
    return {
        "error": "Unknown error in Biome wrapper.",
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": exit_code
    }