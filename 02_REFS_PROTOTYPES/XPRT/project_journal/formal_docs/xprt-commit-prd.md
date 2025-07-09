/*
 * Filename: /Users/antonioreid/01_DOING/XPRT/project_journal/formal_docs/xprt-commit-prd.md
 * Path: /Users/antonioreid/01_DOING/XPRT
 * Created Date: Thursday, April 10th 2025, 9:43:17 pm
 * Author: Antonio J. Reid
 * 
 * Copyright (c) 2025 10xAigency
 */

# Product Requirements Document: xprt-commit

**Version:** 1.0
**Date:** 2025-04-10
**Status:** Draft

## 1. Introduction

`xprt-commit` is a Terminal User Interface (TUI) application designed to streamline the Git commit process for developers, initially within the XPRT monorepo. It aims to enforce conventional commit standards, integrate automated linting and fixing using AI, and provide a user-friendly interface for managing commits. Future versions may expand to include GitHub Pull Request and Issue management.

## 2. Goals

- **Standardize Commit Messages:** Enforce the use of Conventional Commits format.
- **Improve Code Quality:** Integrate multiple linters (Eslint, Prettier, Pylint, Biome.js, GPT Lint) to catch errors before committing.
- **Automate Fixes:** Leverage AI (Gemma3 via Ollama) to suggest and apply fixes for linting errors automatically.
- **Streamline Workflow:** Provide a single TUI to guide developers through staging, linting, fixing, and committing changes.
- **Enhance Developer Experience:** Offer an intuitive and efficient alternative to manual commit steps and linting checks.

## 3. Target Audience

- **Primary:** Developers working within the XPRT monorepo.
- **Secondary:** Potentially any developer using Git who desires a more structured and automated commit workflow.

## 4. Features

### 4.1 MVP (Minimum Viable Product) Scope

The MVP focuses solely on the core commit generation and linting/fixing workflow.

- **TUI Main Menu:**
  - Built using the Textual Python framework.
  - Options:
    - `[➡️] Generate Commit` (Primary MVP focus)
    - `[⚙️] Configuration` (Basic settings if needed for Ollama/linters)
    - `[🔜] Pull Requests` (Placeholder/Disabled)
    - `[🔜] Issues` (Placeholder/Disabled)
- **Commit Generation Workflow:**
  1.  **Initiation:** User selects "Generate Commit" from the main menu.
  2.  **Type/Scope Selection:**
      - The application integrates with the `cz-g` commitizen adapter.
      - A TUI interface (list selection via arrow keys/mouse) prompts the user to select a conventional commit type (e.g., `feat`, `fix`, `chore`).
      - Prompts for an optional scope.
  3.  **Initial Linting:**
      - The application runs configured linters (Eslint, Prettier, Pylint, Biome.js, GPT Lint) on all staged code changes.
  4.  **Error Presentation & Autofix Selection:**
      - If linting errors are found, they are collected and displayed clearly within the TUI, grouped by linter/file.
      - The user can select specific errors (or groups of errors) they want the AI to attempt autofixing for using checkboxes or similar TUI elements.
      - Option to proceed without fixing (if feasible) or cancel.
  5.  **AI Autofix Attempt:**
      - If the user selects errors for autofixing, the application prompts a local Gemma3 model (via Ollama).
      - The prompt includes the code snippets with errors and the corresponding linter output/messages.
      - The goal is for Gemma3 to generate the corrected code.
      - The application applies the suggested fixes from Gemma3 to the relevant files.
  6.  **Re-Linting Loop:**
      - After applying fixes, the application automatically re-runs the linters on the modified files (Step 3).
      - The workflow loops back to Error Presentation (Step 4).
      - This loop continues until:
        - No linting errors remain.
        - The user cancels the process.
        - An unfixable state is reached (TBD definition).
  7.  **Commit Message Generation:**
      - Once the code is lint-free (or the user chooses to proceed despite warnings, if applicable), the application prompts Gemma3 (via Ollama).
      - The prompt includes the selected commit type/scope and the `git diff --staged` output.
      - The goal is for Gemma3 to generate a concise and descriptive commit message body adhering to conventional commit standards.
  8.  **Commit Confirmation:**
      - The generated commit message (header from type/scope, body from Gemma3) is presented to the user for review in the TUI.
      - User confirms or edits the message.
  9.  **Git Commit Execution:**
      - Upon confirmation, the application executes `git commit` with the finalized message.
  10. **Completion:** Returns the user to the main menu or exits, displaying a success message.

### 4.2 Post-MVP Features

- **GitHub Integration:**
  - **Pull Request Management:** View, create, checkout, and potentially comment on Pull Requests associated with the repository directly from the TUI.
  - **Issue Management:** View, create, assign, and potentially comment on Issues associated with the repository directly from the TUI.
- **Configuration Enhancements:** More robust configuration options via the TUI or a config file (e.g., Ollama endpoint, model selection, linter paths/configs).
- **Staging Assistance:** TUI interface for reviewing unstaged changes and selecting files/hunks to stage (`git add -p` equivalent).

## 5. Technical Requirements

- **Programming Language:** Python (>=3.10 recommended for Textual)
- **TUI Framework:** Textual
- **LLM Interaction:** Local Ollama instance running the Gemma3 model.
- **Commitizen:** Integration with `cz-g` Python package (or similar conventional commit helper).
- **Linters:** Ability to invoke and parse output from:
  - Eslint (JavaScript/TypeScript)
  - Prettier (Code formatting)
  - Pylint (Python)
  - Biome.js (JavaScript/TypeScript/JSON)
  - GPT Lint (AI-based linting, specific integration TBD)
- **Platform:** Cross-platform (macOS, Linux, Windows WSL) compatible.
- **Code Location:** To be developed within the `packages/xprt-commit` directory of the XPRT monorepo.

## 6. Non-Functional Requirements

- **Performance:** The TUI must be responsive. Linting and AI interactions should provide feedback and not block the UI indefinitely. Aim for reasonable execution times for fixing and commit generation.
- **Usability:** The TUI should be intuitive and navigable using both keyboard and mouse (where supported by Textual). Clear feedback should be provided at each step.
- **Reliability:** Gracefully handle errors during linting, AI communication (Ollama unavailable), Git operations, and file operations.
- **Maintainability:** Code should be well-structured, documented, and include unit/integration tests where appropriate.
- **Configurability:** Allow basic configuration (e.g., Ollama endpoint) easily.

## 7. Open Questions

- How to handle conflicts if AI autofixes introduce breaking changes? (Manual review step? Diff view?)
- Specific strategy for prompting Gemma3 for optimal autofixing and commit message generation?
- How to configure/discover the paths and configurations for the various linters within the monorepo context?
- Define criteria for "unfixable state" in the lint/autofix loop.
- Error handling strategy if `git commit` fails?
- Exact requirements for the `Configuration` menu in the MVP?
- How will GPT Lint be integrated and invoked? (API key? Local model?)
