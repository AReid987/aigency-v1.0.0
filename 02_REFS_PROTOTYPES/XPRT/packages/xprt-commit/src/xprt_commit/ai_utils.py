#
# File: ai_utils.py                                                           #
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
ai_utils.py

Provides integration functions for calling the Ollama (Gemma3) AI model to generate code fixes.

Author: Roo
Created: 2025-04-12
"""

import subprocess
import logging
import os
from typing import Optional, Dict, Any

try:
    import httpx
except ImportError:
    print("[xprt-commit] Error: httpx is not installed. Please install it with 'pdm add httpx'")
    httpx = None

log = logging.getLogger(__name__)

def execute_command(command: str, cwd: str = None) -> dict:
    """
    Executes a shell command using subprocess.

    Args:
        command (str): The command to execute.
        cwd (str, optional): The working directory in which to execute the command. Defaults to None.

    Returns:
        dict: A dictionary containing the return code, stdout, and stderr.
             Returns None if an exception occurs.
    """
    try:
        env = os.environ.copy()
        log.debug(f"Executing command: {command} in cwd: {cwd}")

        process = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            executable="/bin/bash"  # Specify bash explicitly
        )

        stdout, stderr = process.communicate()
        return_code = process.returncode

        log.debug(f"Command exited with code: {return_code}")
        log.debug(f"Stdout: {stdout}")
        log.debug(f"Stderr: {stderr}")

        return {
            "return_code": return_code,
            "stdout": stdout,
            "stderr": stderr,
            "output": stdout  # For backwards compatibility and simplified access
        }
    except FileNotFoundError as e:
        log.error(f"Command not found: {e}")
        return {
            "return_code": 127,
            "stdout": "",
            "stderr": str(e),
            "output": ""
        }
    except Exception as e:
        log.error(f"Error executing command: {e}", exc_info=True)
        return None


OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Adjust if needed

def build_ollama_prompt(code: str, error: Dict[str, Any]) -> str:
    """
    Build a prompt for the AI code fixer based on the code and lint error.

    Args:
        code (str): Source code snippet or file.
        error (Dict[str, Any]): Lint error dictionary including message, rule, line, etc.

    Returns:
        str: The constructed prompt.
    """
    return (
        f"You are a code fixer AI. Given the following code and lint error, suggest a minimal fix.\n"
        f"---\n"
        f"File: {error.get('file')}\n"
        f"Line: {error.get('line')}\n"
        f"Linter: {error.get('linter')}\n"
        f"Rule: {error.get('ruleId')}\n"
        f"Error: {error.get('message')}\n"
        f"---\n"
        f"Code:\n"
        f"{code}\n"
        f"---\n"
        f"Respond with a unified diff (or if not possible, the full corrected file)."
    )



def build_commit_message_prompt(diff_content: str) -> str:
    """
    Build a prompt for the AI to generate a conventional commit message based on the diff.

    Args:
        diff_content (str): The staged git diff.

    Returns:
        str: The constructed prompt.
    """
    # Basic prompt, can be refined
    return (
        f"You are an expert programmer writing a commit message.\n"
        f"Generate a concise and informative conventional commit message (e.g., 'feat: add new button') "
        f"based *only* on the following git diff:\n"
        f"---\n"
        f"{diff_content}\n"
        f"---\n"
        f"Commit Message:"
    )

def call_ollama_commit_message(diff_content: str, model: str = "gemma3", timeout: float = 60.0) -> Optional[str]:
    """
    Calls the Ollama API with a prompt derived from the diff to generate a commit message.

    Checks for the existence of the specified model before calling the Ollama API.

    Args:
        diff_content (str): The staged git diff content.
        model (str): The Ollama model to use (default: \"gemma3\").
        timeout (float): Request timeout in seconds.

    Returns:
        Optional[str]: The AI's generated commit message, or None/error string on failure.
    """
    try:
        # Check if the model exists
        command_result = execute_command(command=f"ollama list")
        log.info(f"Ollama list command result: {command_result}")
        if command_result is None or command_result.get("return_code") != 0:
            error_detail = command_result.get("stderr", "Unknown error") if command_result else "Command execution failed"
            log.error(f"Error executing 'ollama list': {error_detail}")
            return "[Ollama] Error checking models. Ensure Ollama is running."

        ollama_list_output = command_result.get("output", "")
        log.debug(f"Ollama list output: {ollama_list_output}")
        if model not in ollama_list_output:
            log.warning(f"Ollama model '{model}' not found locally.")
            return f"[Ollama] Model '{model}' not found. Please run 'ollama pull {model}'."

        prompt = build_commit_message_prompt(diff_content)
        log.info(f"Generated commit message prompt (first 100 chars): {prompt[:100]}...")

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        log.debug(f"Payload being sent to Ollama for commit message: {payload}")

        if httpx is None:
            log.error("httpx library is not installed.")
            return "[Ollama] httpx is not installed. Please install it."

        try:
            with httpx.Client() as client:
                response = client.post(OLLAMA_API_URL, json=payload, timeout=timeout)
            log.info(f"Ollama API response status: {response.status_code}")
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            log.debug(f"Ollama API response data: {data}")
            commit_message = data.get("response", "").strip()
            log.info(f"Received commit message suggestion: {commit_message}")
            # Basic cleanup: remove potential markdown code blocks or extra quotes
            if commit_message.startswith("```") and commit_message.endswith("```"):
                commit_message = commit_message[3:-3].strip()
            if commit_message.startswith("'") and commit_message.endswith("'"):
                 commit_message = commit_message[1:-1]
            if commit_message.startswith('"') and commit_message.endswith('"'):
                 commit_message = commit_message[1:-1]
            return commit_message or "[AI failed to generate a message]"
        except httpx.RequestError as exc:
            log.error(f"Ollama API request error: {exc}", exc_info=True)
            return f"[Ollama] Request Error: Could not connect to {OLLAMA_API_URL}. Is Ollama running?"
        except httpx.HTTPStatusError as exc:
            log.error(f"Ollama API HTTP status error: {exc.response.status_code} - {exc.response.text}", exc_info=True)
            return f"[Ollama] HTTP Error: {exc.response.status_code}"
        except Exception as e:
            log.error(f"Ollama API JSON parsing or other error: {e}", exc_info=True)
            return "[Ollama] Error processing API response."

    except Exception as e:
        log.error(f"Error in call_ollama_commit_message: {e}", exc_info=True)
        return "[Ollama] Unexpected error generating commit message."


def call_ollama_code_fix(prompt: str, model: str = "gemma3", timeout: float = 60.0) -> Optional[str]:
    """
    Calls the Ollama API with the given prompt and returns the AI's response.

    Checks for the existence of the gemma3 model before calling the Ollama API and prompts the user to pull it if it's not found.

    Args:
        prompt (str): The prompt to send to the AI model.
        model (str): The Ollama model to use (default: "gemma3").
        timeout (float): Request timeout in seconds.

    Returns:
        Optional[str]: The AI's response (diff or file), or None on failure.
    """
    try:
        # Check if the model exists
        command_result = execute_command(command="ollama list")
        log.info(f"Ollama list command result: {command_result}")
        if command_result is None:
            return "[Ollama] Error executing 'ollama list'. Please ensure Ollama is installed and accessible."

        ollama_list_output = command_result.get("output", "")
        log.info(f"Ollama list output: {ollama_list_output}")
        if "gemma3" not in ollama_list_output:
            return "[Ollama] Model 'gemma3' not found. Please run 'ollama pull gemma3'."

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        log.info(f"Payload being sent to Ollama: {payload}")

        if httpx is None:
            return "[Ollama] httpx is not installed. Please install it with 'pdm add httpx'"

        try:
            response = httpx.post(OLLAMA_API_URL, json=payload, timeout=timeout)
            log.info(f"Ollama API response: {response}")
            response.raise_for_status()
            data = response.json()
            log.info(f"Ollama API data: {data}")
            return data.get("response")
        except Exception as e:
            log.error(f"Ollama API error: {e}", exc_info=True)
            return None

    except Exception as e:
        log.error(f"Error in call_ollama_code_fix: {e}", exc_info=True)
        return None