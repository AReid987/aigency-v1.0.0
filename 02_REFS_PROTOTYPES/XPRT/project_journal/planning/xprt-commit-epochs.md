/*
 * Filename: /Users/antonioreid/01_DOING/XPRT/project_journal/planning/xprt-commit-epochs.md
 * Path: /Users/antonioreid/01_DOING/XPRT
 * Created Date: Thursday, April 10th 2025, 9:44:34 pm
 * Author: Antonio J. Reid
 * 
 * Copyright (c) 2025 10xAigency
 */

# xprt-commit Development Epochs (MVP Focus)

This document outlines the major development phases (Epochs) for the Minimum Viable Product (MVP) of the `xprt-commit` tool, based on the requirements defined in `project_journal/formal_docs/xprt-commit-prd.md`.

---

## Epoch 1: Core TUI & Setup

**Description:** Establish the basic Textual application structure using the Textual framework. Implement the main menu with placeholder options for future features (`Pull Requests`, `Issues`) and basic navigation. Set up initial configuration handling (e.g., loading paths or settings needed for linters and the Ollama endpoint).

**Key Features:**

- Basic Textual app skeleton.
- Main menu screen (`Generate Commit`, `Configuration`, `Pull Requests` [disabled], `Issues` [disabled]).
- Rudimentary configuration loading/parsing.

---

## Epoch 2: Commit Type & Initial Linting

**Description:** Integrate the `cz-g` commitizen adapter (or similar) to provide a TUI for selecting the conventional commit type and optional scope. Implement the logic to identify staged files using Git commands and execute the configured suite of linters (Eslint, Prettier, Pylint, Biome.js, GPT Lint) against these files. Capture and store the linting results.

**Key Features:**

- TUI for commit type/scope selection (integrating `cz-g`).
- Logic to get staged files (`git diff --staged --name-only`).
- Functions to run each configured linter as a subprocess.
- Parsing and aggregation of linting results (errors/warnings).

---

## Epoch 3: Error Display & Autofix Selection

**Description:** Develop the TUI components necessary to display the aggregated linting errors clearly to the user. Errors should be grouped logically (e.g., by file, by linter). Implement interactive elements (like checkboxes or list selections) allowing the user to choose which specific errors or files they want the AI to attempt to autofix. Include options to proceed without fixing or cancel the process.

**Key Features:**

- TUI screen/widget to display formatted lint errors.
- Interactive selection mechanism for errors/files to be autofixed.
- Control flow for proceeding or cancelling.

---

## Epoch 4: AI Autofix Integration

**Description:** Implement the core AI interaction for fixing lint errors. This involves constructing appropriate prompts for the local Gemma3 model (via Ollama) containing the relevant code snippets and linter messages for the selected errors. Process the AI's response, extract the suggested code fixes, and apply these patches carefully to the user's working files.

**Key Features:**

- Ollama client integration.
- Prompt engineering for code fixing based on lint errors.
- Parsing AI responses to extract code changes.
- Applying generated patches to files.
- Error handling for AI interaction failures or invalid patches.

---

## Epoch 5: Re-Linting Loop & Commit Message Generation

**Description:** Implement the iterative loop where, after AI autofixes are applied, the modified files are automatically re-linted (returning to Epoch 3 for error display/selection). This loop continues until no errors remain or the user cancels. Once linting is successful, implement the AI interaction to generate a descriptive commit message body. This involves prompting Gemma3 with the commit type/scope and the final staged `git diff`.

**Key Features:**

- Control flow for the lint-fix-re-lint cycle.
- Termination conditions for the loop (no errors, user cancel, potentially max attempts).
- Prompt engineering for commit message body generation based on diff.
- Parsing AI response for the commit message body.

---

## Epoch 6: Commit Confirmation & Execution

**Description:** Develop the final TUI screen to present the complete, generated commit message (header from Epoch 2, body from Epoch 5) to the user for review. Allow the user to edit the message if necessary before confirmation. Upon confirmation, execute the `git commit -m "..."` command with the finalized message. Provide feedback on success or failure.

**Key Features:**

- TUI screen for commit message review and editing.
- Execution of the `git commit` command.
- Displaying success or error messages to the user.
- Returning to the main menu or exiting gracefully.
