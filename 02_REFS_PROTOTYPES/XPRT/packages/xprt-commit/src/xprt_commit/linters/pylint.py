#
 # File: pylint.py                                                             #
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




import subprocess
import json
from typing import List, Union, Dict, Any, Tuple, Optional


def run_pylint(
    file_paths: List[str],
    pylint_executable: str = "pylint",
    extra_args: Optional[List[str]] = None
) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Run pylint on the given Python files and return a list of issue dictionaries.

    Args:
        file_paths (List[str]): List of Python file paths to lint.
        pylint_executable (str): The pylint command to run (default: "pylint").
        extra_args (Optional[List[str]]): Additional arguments for pylint.

    Returns:
        List[Dict[str, Any]]: List of pylint issues (parsed from JSON output).
        Dict[str, Any]: If an error occurs, returns a dict with 'error' and details.

    Error Handling:
        - If pylint is not found, returns {'error': 'command_not_found', ...}
        - If pylint exits non-zero but outputs JSON, returns the issues.
        - If JSON cannot be parsed, returns {'error': 'json_parse_error', ...}
        - If other subprocess errors occur, returns {'error': 'subprocess_error', ...}
    """
    if not file_paths:
        return []

    command = [pylint_executable, "--output-format=json"]
    if extra_args:
        command += extra_args
    command += file_paths

    try:
        proc = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8"
        )
    except FileNotFoundError:
        return {
            "error": "command_not_found",
            "message": f"Could not find '{pylint_executable}'. Is pylint installed and on your PATH?",
            "command": command,
        }
    except Exception as e:
        return {
            "error": "subprocess_error",
            "message": str(e),
            "command": command,
        }

    stdout = proc.stdout.strip()
    stderr = proc.stderr.strip()
    exit_code = proc.returncode

    # Pylint returns non-zero even if only lint errors are found, so we parse output regardless of exit code.
    try:
        issues = json.loads(stdout) if stdout else []
        return issues
    except json.JSONDecodeError as e:
        return {
            "error": "json_parse_error",
            "message": str(e),
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": exit_code,
            "command": command,
        }