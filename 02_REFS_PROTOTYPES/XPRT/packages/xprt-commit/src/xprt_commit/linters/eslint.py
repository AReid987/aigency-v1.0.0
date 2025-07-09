#
# File: eslint.py                                                             #
# Project: @xprt/xprt-commit                                                  #
# Created Date: Fri Apr 12 2025                                               #
# Author: Roo                                                                 #
# -----                                                                       #
# Last Modified: Fri Apr 12 2025                                              #
# Modified By: Roo                                                            #
# -----                                                                       #
# Copyright (c) 2025 10xAigency                                               #
# -----                                                                       #
# HISTORY:                                                                    #
# Date      	By	Comments                                                   #
# ----------	---	--------------------------------------------------------- #
# 2025-04-12    Roo Initial implementation based on XPRTC-TASK-009.           #

import subprocess
import json
from typing import List, Dict, Any, Optional

def run_eslint(file_paths: List[str]) -> Dict[str, Any]:
    """
    Runs ESLint on the provided files and parses the JSON output.

    Args:
        file_paths (List[str]): List of file paths to lint.

    Returns:
        Dict[str, Any]: {
            'success': bool,  # Indicates if the linting process executed without operational errors.
                            # True even if linting issues were found (exit code 1).
            'issues': List[Dict[str, Any]], # Standardized list of issues.
            'stdout': str,    # Raw stdout from the eslint process.
            'stderr': str,    # Raw stderr from the eslint process.
            'error': Optional[str] # Description of operational errors (e.g., command not found, config error).
        }
        The 'issues' list contains dictionaries of the format:
        {
            'file': str,      # Path to the file with the issue.
            'line': int,      # Line number of the issue.
            'column': int,    # Column number of the issue.
            'message': str,   # Description of the issue.
            'ruleId': Optional[str] # ESLint rule ID, if available.
        }
    """
    result: Dict[str, Any] = {
        'success': False,
        'issues': [],
        'stdout': '',
        'stderr': '',
        'error': None,
    }

    if not file_paths:
        result['error'] = 'No files provided to run ESLint.'
        # Keep success=False as it's an operational error (invalid input)
        return result

    # Consider using 'npx', 'eslint' if eslint isn't globally available or project-local setup is preferred.
    cmd = ['eslint', '--format', 'json'] + file_paths

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,  # Handle exit codes manually
            encoding='utf-8' # Ensure consistent encoding
        )
        result['stdout'] = proc.stdout
        result['stderr'] = proc.stderr

        if proc.returncode == 0:
            # ESLint ran successfully and found no issues.
            result['success'] = True
            result['issues'] = [] # Explicitly set to empty list
        elif proc.returncode == 1:
            # ESLint ran successfully but found linting issues.
            result['success'] = True # Process itself succeeded
            try:
                eslint_output = json.loads(proc.stdout)
                standardized_issues = []
                for file_result in eslint_output:
                    file_path = file_result.get('filePath', 'Unknown File')
                    for message in file_result.get('messages', []):
                        standardized_issues.append({
                            'file': file_path,
                            'line': message.get('line'),
                            'column': message.get('column'),
                            'message': message.get('message', 'Unknown error'),
                            'ruleId': message.get('ruleId')
                        })
                result['issues'] = standardized_issues
            except json.JSONDecodeError as e:
                result['success'] = False # Parsing failure is an operational error
                result['error'] = f'Failed to parse ESLint JSON output (Exit Code 1): {str(e)}\nRaw Output:\n{proc.stdout}'
            except Exception as e: # Catch potential issues during transformation
                 result['success'] = False
                 result['error'] = f'Error processing ESLint output: {str(e)}'
        else:
            # ESLint failed due to configuration error or other issue (Exit Code > 1)
            result['success'] = False
            result['error'] = (
                f'ESLint failed with exit code {proc.returncode}.\n'
                f'Stderr:\n{proc.stderr}\n'
                f'Stdout:\n{proc.stdout}'
            )

    except FileNotFoundError:
        result['success'] = False
        result['error'] = 'ESLint command not found. Please ensure ESLint is installed and accessible in your PATH.'
    except Exception as e:
        result['success'] = False
        result['error'] = f'An unexpected error occurred while running ESLint: {str(e)}'

    return result

# Example usage (for testing purposes):
if __name__ == '__main__':
    # Create dummy files for testing
    dummy_files = ['dummy_ok.js', 'dummy_error.js']
    with open('dummy_ok.js', 'w') as f:
        f.write("console.log('Hello world');\n") # Should pass default rules
    with open('dummy_error.js', 'w') as f:
        f.write("var x = 1;\nconsole.log('Error here')\n") # 'var' might trigger default rules, missing semicolon

    print(f"Running ESLint on: {dummy_files}")
    lint_results = run_eslint(dummy_files)
    print("\n--- Results ---")
    print(f"Success: {lint_results['success']}")
    print(f"Error: {lint_results['error']}")
    print("\nIssues:")
    if lint_results['issues']:
        for issue in lint_results['issues']:
            print(f"  - File: {issue['file']}, Line: {issue['line']}, Col: {issue['column']}, Rule: {issue['ruleId']}, Msg: {issue['message']}")
    else:
        print("  No issues found or parsing failed.")

    print("\nStdout:")
    print(lint_results['stdout'])
    print("\nStderr:")
    print(lint_results['stderr'])

    # Clean up dummy files
    import os
    os.remove('dummy_ok.js')
    os.remove('dummy_error.js')