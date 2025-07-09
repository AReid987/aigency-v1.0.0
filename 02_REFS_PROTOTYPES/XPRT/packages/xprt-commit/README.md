/*
 * Filename: /Users/antonioreid/01_DOING/current-projects/XPRT/packages/xprt-commit/README.md
 * Path: /Users/antonioreid/01_DOING/current-projects/XPRT/packages/xprt-commit
 * Created Date: Thursday, April 10th 2025, 11:08:44 pm
 * Author: Antonio J. Reid
 * 
 * Copyright (c) 2025 10xAigency
 */

# xprt-commit 🚀

Your AI-powered Git commit sidekick! `xprt-commit` streamlines your commit workflow by integrating linting, AI-driven autofixes, and commit message generation directly into a smooth Textual TUI experience.

## ✨ Features

- **Lint Integration:** Automatically runs configured linters (like Ruff, Prettier, etc.) on your staged files before committing.
- **Interactive Error Fixing (TUI):**
  - Displays lint errors clearly grouped in a Textual interface.
  - Select errors you want to fix.
  - Hit "Autofix Selected" to let the AI (powered by Ollama) attempt to fix the selected issues.
- **Autofix & Re-lint Loop:**
  - After attempting fixes, `xprt-commit` automatically re-runs the linters.
  - The TUI updates with remaining errors.
  - This loop continues until all errors are fixed or you decide to cancel. 💪
- **Commit Message Generation:**
  - Once linting passes, get AI-suggested commit messages based on your changes.
  - Option to write your own message or edit the suggestion.
- **TUI Commit Workflow:** Guides you through reviewing the final changes and confirming the commit, all within the TUI.

## ⚙️ How it Works (The Flow)

1.  **Run `xprt-commit`:** (Assuming it's aliased or on PATH) When you're ready to commit staged changes.
2.  **Linting:** Linters run automatically.
3.  **Error TUI (If Errors):**
    - If errors are found, the `LintErrorDisplayScreen` pops up.
    - Navigate and select errors using arrow keys and spacebar.
    - Choose `Autofix Selected`. The AI works its magic. ✨
    - Linters re-run. The TUI updates.
    - Repeat until no errors remain, or `Cancel`.
4.  **Commit Message TUI (No Errors):**
    - The `CommitMessageScreen` appears.
    - View AI-suggested messages (if configured) or type your own.
    - Review and confirm the message.
5.  **Commit:** `xprt-commit` performs the `git commit` operation.
6.  **Done!** 🎉

## 🚀 Usage

_(Assuming installation and basic configuration are done)_

```bash
# Stage your changes first
git add .

# Run the tool
xprt-commit
```

Follow the on-screen prompts in the TUI to navigate the linting, fixing, and commit process.

## 🛠️ Configuration

_(Details on configuring linters, AI models, etc., will go here in the future)_

---

Enjoy cleaner code and smoother commits!
