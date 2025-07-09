# DevLog-XPRT Project Setup with Commitizen and Git Hooks

This document outlines the setup of our project with commitizen, lint-staged, and lefthook for standardized commit messages and code quality checks.

## Installed Dependencies

- pnpm: Package manager
- dotenv-vault: Environment variable management
- commitizen: Interactive commit message CLI
- cz-git: Commitizen adapter with AI capabilities
- czg: CLI tool for cz-git
- lefthook: Git hooks manager
- @commitlint/cli and @commitlint/config-conventional: For commit message linting
- enquirer: Interactive CLI prompts for our custom AI commit script
- lint-staged: Run linters on git staged files

## Commit Message Configuration

We've set up commitizen with cz-git to:
- Use emoji in commit messages
- Support multiple scopes with checkboxes
- Automatically detect scopes from apps and packages directories
- Integrate with Gemma 3 via Ollama for AI-assisted commit messages

## Using the Commit Flow

For regular interactive commits:

```bash
pnpm commit
```

For AI-assisted commit messages with Gemma 3:

```bash
pnpm commit:ai
```

The commit flow will:
1. Prompt you to select a commit type (feat, fix, docs, etc.)
2. Allow you to select one or more scopes from a checkbox list
3. Help you write a commit message (with AI assistance when using `commit:ai`)
4. Add appropriate emojis based on the commit type

## Git Hooks

We use lefthook for managing git hooks:

- **commit-msg**: Validates commit messages against commitlint rules
- **pre-commit**: Runs lint-staged to check only the staged files

## Lint-Staged Configuration

Lint-staged is configured to:
- Format all staged files with Prettier
- Lint JavaScript/TypeScript files with ESLint
- Type check TypeScript files with TypeScript

This ensures that only the files you're committing are checked, making the process faster and more efficient.

## Ollama Setup

To use Gemma 3 for AI-assisted commit messages:

1. Install Ollama: https://ollama.com/
2. Pull the Gemma 3 model: `ollama pull gemma3`
3. Make sure Ollama is running when you use `pnpm commit:ai`

## Custom AI Commit Script

We've created a custom script for AI-assisted commits that bypasses git hooks:

1. The script is located at `scripts/commit-ai.sh`
2. It uses Ollama's API to generate commit messages based on staged changes
3. Run it with `pnpm commit:ai`

The script will:
1. Check if there are staged changes
2. Present an interactive menu to select a commit type using arrow keys
3. Show a checkbox selection for scopes (automatically detected from apps and packages)
4. Send the git diff to Ollama's Gemma 3 model
5. Generate a commit message based on the changes
6. Ask if you want to use the generated message
7. Create the commit with the selected message

### Troubleshooting

If you encounter issues with the Ollama API response, the script will fall back to a default commit message. Common issues include:
- Ollama not running (start with `ollama serve`)
- Network connectivity issues
- Unexpected API response format
- Timeout issues with large diffs

## Configuration Files

- **package.json**: Contains commitizen configuration and commit scripts
- **commitlint.config.js**: Contains commitlint configuration for validating commit messages
- **lefthook.yml**: Git hooks configuration
- **.lintstagedrc.js**: Lint-staged configuration for checking staged files
- **scripts/commit-ai.sh**: Custom script for AI-assisted commits
- **scripts/generate-commit-message.js**: Node.js script that interacts with Ollama
