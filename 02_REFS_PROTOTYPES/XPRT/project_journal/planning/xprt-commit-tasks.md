/*
 * Filename: /Users/antonioreid/01_DOING/XPRT/project_journal/planning/xprt-commit-tasks.md
 * Path: /Users/antonioreid/01_DOING/XPRT
 * Created Date: Thursday, April 10th 2025, 9:46:12 pm
 * Author: Antonio J. Reid
 * 
 * Copyright (c) 2025 10xAigency
 */

# xprt-commit MVP - Detailed Development Tasks

This document breaks down the Epochs defined in `project_journal/planning/xprt-commit-epochs.md` into specific, actionable development tasks for the MVP.

---

## Epoch 1: Core TUI & Setup

**Goal:** Establish the basic Textual application structure, main menu, and configuration handling.

**Tasks:**

- `XPRTC-TASK-001`: Initialize Textual application structure (e.g., `src/xprt_commit/main.py`).
- `XPRTC-TASK-002`: Implement Main Menu screen using Textual (`src/xprt_commit/screens/main_menu.py`).
  - Include options: "Generate Commit", "Configuration", "Pull Requests" (disabled/placeholder), "Issues" (disabled/placeholder).
- `XPRTC-TASK-003`: Implement basic navigation logic between Main Menu and other (placeholder) screens/actions (`src/xprt_commit/app.py`).
- `XPRTC-TASK-004`: Implement Configuration screen skeleton (`src/xprt_commit/screens/config_screen.py`). (Dependency: `XPRTC-TASK-001`)
- `XPRTC-TASK-005`: Define initial configuration structure (e.g., in `config.toml` or Python dict). Include basic settings like Ollama endpoint URL and potentially paths for tools.
- `XPRTC-TASK-006`: Implement configuration loading/parsing logic (`src/xprt_commit/config.py`).

---

## Epoch 2: Commit Type & Initial Linting

**Goal:** Integrate commit type selection, identify staged files, and run configured linters.

**Tasks:**

- `XPRTC-TASK-007`: Integrate `cz-g` or similar library/logic for Conventional Commit type/scope selection via TUI (`src/xprt_commit/screens/commit_type_screen.py`). (Dependency: `XPRTC-TASK-001`)
- `XPRTC-TASK-008`: Implement utility function to get staged files using `git diff --staged --name-only` (`src/xprt_commit/git_utils.py`).
- `XPRTC-TASK-009`: Implement function wrapper to run Eslint subprocess and capture output (`src/xprt_commit/linters/eslint.py`). (Dependency: `XPRTC-TASK-008`)
- `XPRTC-TASK-010`: Implement function wrapper to run Prettier subprocess and capture output (`src/xprt_commit/linters/prettier.py`). (Dependency: `XPRTC-TASK-008`)
- `XPRTC-TASK-011`: Implement function wrapper to run Pylint subprocess and capture output (`src/xprt_commit/linters/pylint.py`). (Dependency: `XPRTC-TASK-008`)
- `XPRTC-TASK-012`: Implement function wrapper to run Biome.js subprocess and capture output (`src/xprt_commit/linters/biome.py`). (Dependency: `XPRTC-TASK-008`)
- `XPRTC-TASK-013`: Implement function wrapper to run GPT Lint subprocess and capture output (`src/xprt_commit/linters/gptlint.py`). (Dependency: `XPRTC-TASK-008`)
- `XPRTC-TASK-014`: Implement main linting orchestration logic to call enabled linters based on config and file types (`src/xprt_commit/linting.py`). (Dependencies: `XPRTC-TASK-006`, `XPRTC-TASK-009` to `XPRTC-TASK-013`)
- `XPRTC-TASK-015`: Implement parsing logic for each linter's output and aggregate results into a standardized format (e.g., list of dicts with file, line, message) (`src/xprt_commit/linting.py`). (Dependency: `XPRTC-TASK-014`)

---

## Epoch 3: Error Display & Autofix Selection

**Goal:** Display linting errors in the TUI and allow user selection for autofixing.

**Tasks:**

- `XPRTC-TASK-016`: Define the standardized data structure for aggregated lint errors. (Dependency: `XPRTC-TASK-015`)
- `XPRTC-TASK-017`: Implement Textual screen/widget to display formatted lint errors, ideally grouped by file and/or linter (`src/xprt_commit/screens/error_display.py`). (Dependency: `XPRTC-TASK-016`)
- `XPRTC-TASK-018`: Implement interactive selection mechanism (e.g., Textual `Checkbox`, `DataTable`, or `ListView`) in the error display screen for choosing errors/files to fix (`src/xprt_commit/screens/error_display.py`). (Dependency: `XPRTC-TASK-017`)
- `XPRTC-TASK-019`: Implement control flow buttons/actions (e.g., "Autofix Selected", "Proceed without Fixing", "Cancel") on the error display screen and connect them to the application logic (`src/xprt_commit/screens/error_display.py`). (Dependency: `XPRTC-TASK-018`)

---

## Epoch 4: AI Autofix Integration

**Goal:** Integrate with Ollama (Gemma3) to attempt autofixing selected lint errors.

**Tasks:**

- `XPRTC-TASK-020`: Implement Ollama client setup and a function for basic chat completion requests (`src/xprt_commit/ai_utils.py`). (Dependency: `XPRTC-TASK-006`)
- `XPRTC-TASK-021`: Develop prompt template(s) for code fixing, including context (code snippet, error message) (`src/xprt_commit/prompts.py`).
- `XPRTC-TASK-022`: Implement function to construct specific prompts for selected errors using the template and relevant file content (`src/xprt_commit/ai_utils.py`). (Dependencies: `XPRTC-TASK-018`, `XPRTC-TASK-021`)
- `XPRTC-TASK-023`: Implement function to send prompts to Ollama and retrieve the suggested code fixes (`src/xprt_commit/ai_utils.py`). (Dependencies: `XPRTC-TASK-020`, `XPRTC-TASK-022`)
- `XPRTC-TASK-024`: Implement logic to parse AI responses, extracting the code changes (e.g., assuming diff format or full file replacement) (`src/xprt_commit/ai_utils.py`). (Dependency: `XPRTC-TASK-023`)
- `XPRTC-TASK-025`: Implement utility function to apply extracted patches/changes to the relevant files in the working directory (`src/xprt_commit/file_utils.py`). (Dependency: `XPRTC-TASK-024`)
- `XPRTC-TASK-026`: Add robust error handling for Ollama API calls (timeouts, connection errors, model errors) (`src/xprt_commit/ai_utils.py`). (Dependency: `XPRTC-TASK-023`)
- `XPRTC-TASK-027`: Add validation and error handling for applying patches (e.g., patch apply failure, file not found) (`src/xprt_commit/file_utils.py`). (Dependency: `XPRTC-TASK-025`)

---

## Epoch 5: Re-Linting Loop & Commit Message Generation

**Goal:** Implement the lint-fix-re-lint cycle and generate the commit message body using AI.

**Tasks:**

- `XPRTC-TASK-028`: Implement the main application control flow for the lint -> select -> fix -> re-lint cycle (`src/xprt_commit/app.py` or main orchestrator). (Dependencies: `XPRTC-TASK-014`, `XPRTC-TASK-019`, `XPRTC-TASK-025`)
- `XPRTC-TASK-029`: Define and implement termination conditions for the re-linting loop (e.g., no errors found, user cancels, maximum attempts reached) (`src/xprt_commit/app.py`). (Dependency: `XPRTC-TASK-028`)
- `XPRTC-TASK-030`: Implement utility function to get the final staged `git diff` after all fixes have been applied (`src/xprt_commit/git_utils.py`). (Dependency: `XPRTC-TASK-025` or loop completion)
- `XPRTC-TASK-031`: Develop prompt template for generating the commit message body, using commit type/scope and the final git diff (`src/xprt_commit/prompts.py`).
- `XPRTC-TASK-032`: Implement function to construct the commit message generation prompt (`src/xprt_commit/ai_utils.py`). (Dependencies: `XPRTC-TASK-007`, `XPRTC-TASK-030`, `XPRTC-TASK-031`)
- `XPRTC-TASK-033`: Implement function call to Ollama for commit message generation (`src/xprt_commit/ai_utils.py`). (Dependencies: `XPRTC-TASK-020`, `XPRTC-TASK-032`)
- `XPRTC-TASK-034`: Implement parsing of the AI response to extract the generated commit message body (`src/xprt_commit/ai_utils.py`). (Dependency: `XPRTC-TASK-033`)

---

## Epoch 6: Commit Confirmation & Execution

**Goal:** Present the generated commit message for review/edit and execute the git commit.

**Tasks:**

- `XPRTC-TASK-035`: Implement Textual screen for displaying the complete generated commit message (header from Epoch 2 + body from Epoch 5) (`src/xprt_commit/screens/commit_confirm.py`). (Dependencies: `XPRTC-TASK-007`, `XPRTC-TASK-034`)
- `XPRTC-TASK-036`: Implement editing capability (e.g., using Textual `TextArea`) within the commit confirmation screen (`src/xprt_commit/screens/commit_confirm.py`). (Dependency: `XPRTC-TASK-035`)
- `XPRTC-TASK-037`: Implement function to execute `git commit -m "..."` using the final, potentially edited, message (`src/xprt_commit/git_utils.py`). (Dependency: `XPRTC-TASK-036`)
- `XPRTC-TASK-038`: Implement display of success or failure message after the commit attempt within the TUI (`src/xprt_commit/screens/commit_confirm.py` or app status bar). (Dependency: `XPRTC-TASK-037`)
- `XPRTC-TASK-039`: Implement final application flow logic to either return to the main menu or exit gracefully after commit completion/failure (`src/xprt_commit/app.py`). (Dependency: `XPRTC-TASK-038`)

---
