#
 # File: linting.py                                                            #
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
Module: linting.py

Provides orchestration and aggregation for all available linter wrappers in xprt-commit.
Runs enabled linters on a set of staged files, normalizes and aggregates their results,
and returns a unified list of issues and errors for display in the TUI.

Author: Roo
Created: 2025-04-12
"""

from typing import List, Dict, Any, Optional
import subprocess
from .eslint import run_eslint
from .prettier import run_prettier_check
try:
    from .pylint import run_pylint
except ImportError:
    run_pylint = None
try:
    from .biome import run_biome
except ImportError:
    run_biome = None
try:
    from .gptlint import run_gptlint
except ImportError:
    run_gptlint = None

def normalize_eslint_issues(eslint_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Normalize ESLint issues to the standard format."""
    issues = []
    for issue in eslint_result.get('issues', []):
        issues.append({
            "linter": "eslint",
            "file": issue.get("file"),
            "line": issue.get("line"),
            "column": issue.get("column"),
            "message": issue.get("message"),
            "ruleId": issue.get("ruleId"),
            "severity": None,  # Could be added if available in future
        })
    return issues

def normalize_prettier_issues(prettier_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Normalize Prettier results to the standard format."""
    issues = []
    if prettier_result.get('needs_formatting') and prettier_result.get('files'):
        for file in prettier_result['files']:
            issues.append({
                "linter": "prettier",
                "file": file,
                "line": None,
                "column": None,
                "message": "File is not formatted according to Prettier rules.",
                "ruleId": None,
                "severity": "warn",
            })
    return issues

def normalize_pylint_issues(pylint_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Normalize PyLint results to the standard format."""
    issues = []
    for issue in pylint_result.get('issues', []):
        issues.append({
            "linter": "pylint",
            "file": issue.get("file"),
            "line": issue.get("line"),
            "column": issue.get("column"),
            "message": issue.get("message"),
            "ruleId": issue.get("symbol") or issue.get("ruleId"),
            "severity": issue.get("type"),
        })
    return issues

def normalize_biome_issues(biome_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Normalize Biome results to the standard format."""
    issues = []
    for issue in biome_result.get('issues', []):
        issues.append({
            "linter": "biome",
            "file": issue.get("file"),
            "line": issue.get("line"),
            "column": issue.get("column"),
            "message": issue.get("message"),
            "ruleId": issue.get("ruleId"),
            "severity": issue.get("severity"),
        })
    return issues

def normalize_gptlint_issues(gptlint_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Normalize GPTLint results to the standard format."""
    issues = []
    for issue in gptlint_result.get('issues', []):
        issues.append({
            "linter": "gptlint",
            "file": issue.get("file"),
            "line": issue.get("line"),
            "column": issue.get("column"),
            "message": issue.get("message"),
            "ruleId": issue.get("ruleId"),
            "severity": issue.get("severity"),
        })
    return issues

def log_error(linter: str, error: str) -> Dict[str, Any]:
    """Format an error as an issue dict for display."""
    return {
        "linter": linter,
        "file": None,
        "line": None,
        "column": None,
        "message": f"[{linter}] ERROR: {error}",
        "ruleId": None,
        "severity": "error",
    }

def run_all_linters(staged_files: List[str], config: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Runs all enabled linters on the provided staged files and aggregates their results.

    Args:
        staged_files (List[str]): List of file paths to lint.
        config (Optional[Dict[str, Any]]): Configuration dictionary. Example:
            {
                "eslint": True,
                "prettier": True,
                "pylint": False,
                "biome": True,
                "gptlint": True
            }
            If None, all available linters are run.

    Returns:
        List[Dict[str, Any]]: Aggregated list of normalized issues and errors.
            Each dict contains:
                - linter: str
                - file: str or None
                - line: int or None
                - column: int or None
                - message: str
                - ruleId: str or None
                - severity: str or None
    """
    results: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []

    enabled_linters = {
        "eslint": config.get("eslint", True) if config else True,
        "prettier": config.get("prettier", True) if config else True,
        "pylint": config.get("pylint", True) if config else True,
        "biome": config.get("biome", True) if config else True,
        "gptlint": config.get("gptlint", True) if config else True,
    }

    # ESLint
    if enabled_linters["eslint"]:
        try:
            eslint_result = run_eslint(staged_files)
            if eslint_result.get("success"):
                results.extend(normalize_eslint_issues(eslint_result))
            if eslint_result.get("error"):
                errors.append(log_error("eslint", eslint_result["error"]))
        except Exception as e:
            errors.append(log_error("eslint", f"Exception: {str(e)}"))

    # Prettier
    if enabled_linters["prettier"]:
        try:
            prettier_result = run_prettier_check(staged_files)
            results.extend(normalize_prettier_issues(prettier_result))
            if prettier_result.get("error"):
                errors.append(log_error("prettier", prettier_result["error"]))
        except Exception as e:
            errors.append(log_error("prettier", f"Exception: {str(e)}"))

    # PyLint
    if enabled_linters["pylint"] and run_pylint:
        try:
            pylint_result = run_pylint(staged_files)
            if pylint_result.get("issues"):
                results.extend(normalize_pylint_issues(pylint_result))
            if pylint_result.get("error"):
                errors.append(log_error("pylint", pylint_result["error"]))
        except Exception as e:
            errors.append(log_error("pylint", f"Exception: {str(e)}"))

    # Biome
    if enabled_linters["biome"] and run_biome:
        try:
            biome_result = run_biome(staged_files)
            if biome_result.get("issues"):
                results.extend(normalize_biome_issues(biome_result))
            if biome_result.get("error"):
                errors.append(log_error("biome", biome_result["error"]))
        except Exception as e:
            errors.append(log_error("biome", f"Exception: {str(e)}"))

    # GPTLint
    if enabled_linters["gptlint"] and run_gptlint:
        try:
            gptlint_result = run_gptlint(staged_files)
            if gptlint_result.get("issues"):
                results.extend(normalize_gptlint_issues(gptlint_result))
            if gptlint_result.get("error"):
                errors.append(log_error("gptlint", gptlint_result["error"]))
        except Exception as e:
            errors.append(log_error("gptlint", f"Exception: {str(e)}"))

    # Combine issues and errors for output
    return results + errors