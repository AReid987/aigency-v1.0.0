#
 # File: gptlint.py                                                            #
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




# File: gptlint.py
# Project: @xprt/xprt-commit
# Created Date: Fri Apr 11 2025
# Author: Antonio J. Reid
# -----
# Copyright (c) 2025 10xAigency
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------

import subprocess
from typing import List, Dict, Any, Optional
import json

def run_gptlint(file_paths: List[str]) -> Dict[str, Any]:
    """
    Runs GPT Lint on the provided files and parses the JSON output.

    Args:
        file_paths (List[str]): List of file paths to lint.

    Returns:
        Dict[str, Any]: {
            'success': bool,
            'issues': list or dict,
            'stdout': str,
            'stderr': str,
            'error': Optional[str]
        }
    """
    result = {
        'success': False,
        'issues': [],
        'stdout': '',
        'stderr': '',
        'error': None,
    }

    if not file_paths:
        result['error'] = 'No files provided to run GPT Lint.'
        return result

    cmd = ['npx', 'gptlint', '--format', 'json'] + file_paths

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        result['stdout'] = proc.stdout
        result['stderr'] = proc.stderr

        if proc.returncode == 0:
            # Lint succeeded, parse JSON output
            try:
                parsed = json.loads(proc.stdout)
                result['issues'] = parsed
                result['success'] = True
            except json.JSONDecodeError as e:
                result['error'] = f'Failed to parse GPT Lint JSON output: {str(e)}'
        elif proc.returncode == 1:
            # Lint found issues, still parse JSON
            try:
                parsed = json.loads(proc.stdout)
                result['issues'] = parsed
            except json.JSONDecodeError as e:
                result['error'] = f'Failed to parse GPT Lint JSON output: {str(e)}'
        else:
            result['error'] = f'GPT Lint failed with exit code {proc.returncode}'
    except FileNotFoundError:
        result['error'] = 'npx or gptlint not found. Please ensure GPT Lint is installed and npx is available.'
    except Exception as e:
        result['error'] = str(e)

    return result