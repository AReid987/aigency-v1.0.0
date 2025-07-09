import subprocess

#
# File: git_utils.py                                                          #
# Project: @xprt/xprt-commit                                                  #
# Created Date: Fr Apr 2025                                                   #
# Author: <<author>                                                           #
# -----                                                                       #
# Last Modified: Tue Apr 15 2025                                              #
# Modified By: Antonio J. Reid                                                #
# -----                                                                       #
# Copyright (c) 2025 10xAigency                                               #
# -----                                                                       #
# HISTORY:                                                                    #
# Date      	By	Comments                                                   #
# ----------	---	---------------------------------------------------------  #



import logging
import os
from typing import List, Dict, Tuple

log = logging.getLogger(__name__)


def get_staged_diff() -> str:
    import subprocess
    try:
        result = subprocess.run(
            ["git", "diff", "--staged"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"[ERROR: Failed to get git diff: {e}]"

def get_staged_files() -> List[str]:
    """
    Retrieves a list of staged files from the Git repository.

    Uses the 'git diff --staged --name-only' command to get the list.

    Returns:
        List[str]: A list of file paths (strings) that are staged.
                   Returns an empty list if the command fails or no files are staged.
    """
    try:
        # Run the git command to get staged files
        result = subprocess.run(
            ['git', 'diff', '--staged', '--name-only'],
            capture_output=True,
            text=True,
            check=True,  # Raises CalledProcessError if the command returns a non-zero exit code
            encoding='utf-8'
        )

        # Split the output into a list of files
        staged_files = result.stdout.strip().split('\n')

        # Filter out empty strings in case of no staged files
        staged_files = [file for file in staged_files if file]

        return staged_files

    except subprocess.CalledProcessError as e:
        # Handle cases where the git command fails (e.g., not a git repo, other errors)
        # Log the error for debugging purposes (optional)
        # print(f"Error running git command: {e}")
        return []
    except FileNotFoundError:
        # Handle case where git command is not found
        # print("Error: 'git' command not found. Is Git installed and in PATH?")
        return []
    except Exception as e:
        # Catch any other potential exceptions
        # print(f"An unexpected error occurred: {e}")
        return []



def get_unstaged_files() -> List[Dict[str, str]]:
    """
    Retrieves a list of unstaged files (modified, untracked, deleted) from the Git repository.

    Uses 'git status --porcelain=v1' command.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing 'status' and 'file' keys.
                               'status' can be ' M' (Modified), '??' (Untracked), ' D' (Deleted).
                               Returns an empty list if the command fails or no unstaged files are found.
    """
    unstaged_files = []
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain=v1'],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )

        lines = result.stdout.strip().split('\n')
        for line in lines:
            if not line:
                continue

            # Format is 'XY path' where Y is the working tree status
            status_code = line[1] # Character at index 1 indicates working tree status
            file_path = line[3:] # Path starts after 'XY '

            # Handle potentially quoted paths for files with spaces
            if file_path.startswith('"') and file_path.endswith('"'):
                file_path = file_path[1:-1].replace('\\"', '"').replace('\\\\', '\\') # Basic unquoting

            if status_code == 'M':
                unstaged_files.append({'status': ' M', 'file': file_path})
            elif status_code == 'D':
                 # Need to check if it's staged for deletion (' D') vs just deleted (' D')
                 # We only care about unstaged deletions (' D')
                 if line[0] == ' ': # Check index status (X)
                    unstaged_files.append({'status': ' D', 'file': file_path})
            elif status_code == '?': # Untracked files have '??'
                if line.startswith('??'):
                    unstaged_files.append({'status': '??', 'file': file_path})
            # Add other statuses if needed (e.g., 'A' for added but not committed, 'R' for renamed, 'C' for copied)
            # For now, focusing on Modified, Untracked, Deleted in the working tree.

        log.info(f"Found unstaged files: {unstaged_files}")
        return unstaged_files

    except subprocess.CalledProcessError as e:
        log.error(f"Error running 'git status --porcelain=v1': {e}")
        return []
    except FileNotFoundError:
        log.error("'git' command not found. Is Git installed and in PATH?")
        return []
    except Exception as e:
        log.error(f"An unexpected error occurred getting unstaged files: {e}", exc_info=True)
        return []


def commit_staged_files(message: str) -> (bool, str):
    """
    Commits staged files with the given commit message.

    Args:
        message (str): The commit message.

    Returns:
        (bool, str): Tuple of (success, output or error message)
    """
    if not message.strip():
        return (False, "Commit message cannot be empty.")
    try:
        result = subprocess.run(
            ['git', 'commit', '-m', message],
            capture_output=True,
            text=True,
            check=False,  # Let us handle errors manually
            encoding='utf-8'
        )
        if result.returncode == 0:
            return (True, result.stdout.strip())
        else:
            return (False, result.stderr.strip() or result.stdout.strip())
    except Exception as e:
        return (False, str(e))


if __name__ == '__main__':
    # Example usage:
    staged = get_staged_files()
    if staged:
        print("Staged files:")
        for file in staged:
            print(f"- {file}")
    else:
        print("No files are staged or an error occurred.")

    print("\nChecking for unstaged files...")
    unstaged = get_unstaged_files()
    if unstaged:
        print("Unstaged files:")
        for item in unstaged:
            print(f"- Status: [{item['status']}], File: {item['file']}")
    else:
        print("No unstaged files found or an error occurred.")

    # Example call to implemented stage_files
    # print("\nAttempting to stage/remove files...")
    # # Create dummy files for testing if they don't exist
    # # with open("file_to_add.txt", "w") as f: f.write("add me")
    # # with open("file_to_remove.txt", "w") as f: f.write("remove me")
    # # subprocess.run(['git', 'add', 'file_to_remove.txt']) # Stage it first
    # # os.remove("file_to_remove.txt") # Then delete it to simulate ' D'
    #
    # success, msg = stage_files(['file_to_add.txt'], ['file_to_remove.txt'])
    # print(f"Staging result: {success} - {msg}")
    #
    # # Clean up dummy files
    # # if os.path.exists("file_to_add.txt"): os.remove("file_to_add.txt")
    # # # file_to_remove.txt should be gone or staged for removal
    # # subprocess.run(['git', 'reset', '--', 'file_to_add.txt', 'file_to_remove.txt']) # Clean git index
    # # subprocess.run(['git', 'checkout', '--', 'file_to_remove.txt']) # Restore deleted file if needed
    # # if os.path.exists("file_to_remove.txt"): os.remove("file_to_remove.txt")


def stage_files(files_to_stage: List[str], files_to_remove: List[str]) -> Tuple[bool, str]:
    """
    Stages specified files using 'git add' and removes specified files using 'git rm'.

    Args:
        files_to_stage: List of file paths to stage.
        files_to_remove: List of file paths to remove (unstage deletion).

    Returns:
        Tuple[bool, str]: (success, message)
    """
    # Implementation will be added later
    # TODO: Implement actual git add/rm logic with error handling
    staged_successfully = []
    removed_successfully = []
    errors = []

    if files_to_stage:
        try:
            cmd = ['git', 'add', '--'] + files_to_stage
            log.info(f"Running command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
            log.info(f"'git add' output: {result.stdout}")
            staged_successfully.extend(files_to_stage)
        except subprocess.CalledProcessError as e:
            err_msg = f"Error staging {files_to_stage}: {e.stderr or e.stdout}"
            log.error(err_msg)
            errors.append(err_msg)
        except Exception as e:
            err_msg = f"Unexpected error staging {files_to_stage}: {e}"
            log.error(err_msg, exc_info=True)
            errors.append(err_msg)

    if files_to_remove:
        try:
            # For unstaged deletions (' D'), we need to use 'git rm' to stage the deletion
            cmd = ['git', 'rm', '--'] + files_to_remove
            log.info(f"Running command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
            log.info(f"'git rm' output: {result.stdout}")
            removed_successfully.extend(files_to_remove)
        except subprocess.CalledProcessError as e:
            # It's possible 'git rm' fails if the file wasn't actually deleted but just unstaged
            # Or if it was already staged for removal. Check status carefully.
            err_msg = f"Error removing {files_to_remove}: {e.stderr or e.stdout}"
            log.warning(err_msg) # Log as warning, might not be critical
            # Attempt to stage potential modifications if rm failed? Or just report? Report for now.
            errors.append(err_msg)
        except Exception as e:
            err_msg = f"Unexpected error removing {files_to_remove}: {e}"
            log.error(err_msg, exc_info=True)
            errors.append(err_msg)

    if errors:
        return (False, "\n".join(errors))
    else:
        msg_parts = []
        if staged_successfully:
            msg_parts.append(f"Staged: {', '.join(staged_successfully)}")
        if removed_successfully:
            msg_parts.append(f"Removed: {', '.join(removed_successfully)}")
        return (True, ". ".join(msg_parts) or "No changes staged/removed.")




def run_lint_staged(fix: bool = False) -> Tuple[bool, str, str]:
    """
    Runs lint-staged on currently staged files.

    Args:
        fix (bool): If True, attempts to autofix issues using `lint-staged --fix`.


    Returns:
        Tuple[bool, str, str]: A tuple containing:
            - bool: True if lint-staged exited with code 0, False otherwise.
            - str: The standard output of the command.
            - str: The standard error of the command.
    """
    log.info("Running lint-staged...")
    try:
        command_parts = ["npx", "lint-staged"]
        if fix:
            command_parts.append("--fix")
        command = " ".join(command_parts)

        log.info(f"Executing command: {command}")
        # Using shell=True with shlex.split is generally discouraged due to security risks,
        # but for running npx which is typically in the user's environment, it's often necessary.
        # A safer alternative would be to find the npx executable path and run it directly.
        # For now, keeping the existing subprocess.run structure with shlex.split.
        process = subprocess.run(shlex.split(command), capture_output=True, text=True, check=False) # nosec
        log.info(f"Command finished with exit code {process.returncode}")
        log.debug(f"STDOUT:\n{process.stdout}")
        log.debug(f"STDERR:\n{process.stderr}")

        return (process.returncode == 0, process.stdout, process.stderr)

    except FileNotFoundError:
        log.error("Error: 'npx' command not found. Make sure Node.js and npm/yarn/pnpm are installed and in your PATH.", exc_info=True)
        return (False, "", "[ERROR: 'npx' command not found]")
    except Exception as e:
        log.error(f"An unexpected error occurred while running lint-staged: {e}", exc_info=True)
        return (False, "", f"An unexpected error occurred: {e}")
