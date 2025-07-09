# XPRT-Commit Task Backlog

- **Task ID: XPRTC-001**

  - **Goal:** Implement check for unstaged files before commit message generation.
  - **Description:** Refine the pre-commit workflow and `StageFilesScreen`:
    1. **Unify Triggers:** Ensure both the 'g' keybinding (`action_generate_commit`) and the "Generate Commit" button trigger the exact same workflow (`start_commit_flow`).
    2. **Initial State Check:** When the flow starts, check for _both_ staged and unstaged files and display their counts (e.g., via `app.notify`).
    3. **Immediate Staging Prompt:** If unstaged files exist, _immediately_ push the `StageFilesScreen`. Don't require a second trigger.
    4. **Enhance `StageFilesScreen`:**
       - Make the file list interactive (e.g., using `DataTable` with selectable rows or a `Checklist`).
       - Add functionality/buttons to "Stage Selected", "Stage All", "Unstage Selected" (if applicable), and "Continue/Skip Staging".
       - Update the displayed staged/unstaged counts dynamically as the user interacts.
    5. **Conditional Linting:** After the `StageFilesScreen` is dismissed (or if there were no unstaged files initially), check if there are _any_ files staged. Only proceed to the linting step (Task XPRTC-002) if files are actually staged. If no files are staged, notify the user and end the flow.

- **Task ID: XPRTC-002**
  - **Goal:** Integrate and sequence linting, autofixing, and AI commit message generation.
  - **Description:** Determine the optimal workflow for running `lint-staged` (which potentially modifies files and runs linters/fixers) and calling the AI (`ollama`) to generate the commit message based on the _final_ staged changes. Implement the chosen sequence within the AI suggestion workflow (`generate_ai_commit_message_worker` or related functions). Consider error handling for each step.
