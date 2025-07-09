/*
 * Filename: /Users/antonioreid/01_DOING/XPRT/packages/xprt-commit/package.json.comments.md
 * Path: /Users/antonioreid/01_DOING/XPRT/packages/xprt-commit
 * Created Date: Friday, April 11th 2025, 3:14:14 am
 * Author: Antonio J. Reid
 * 
 * Copyright (c) 2025 10xAigency
 */

# package.json Explanations for @xprt/xprt-commit

This file explains each section of the `package.json` in this directory.

---

## name, version, type

- **name**: Package name for Turborepo and npm registry. Uses the `@xprt` scope for clarity.
- **version**: Semantic version for tracking releases.
- **type**: `"module"` enables ECMAScript module syntax (import/export).

## description, author

- **description**: Short summary for documentation and registry.
- **author**: Project/maintainer attribution.

## scripts

- **lint**: Runs ESLint on JS/TS/Python files (adjust extensions as needed).
- **format**: Runs Prettier on all files for formatting.
- **lint-staged**: Runs lint-staged (used by lefthook).
- **commit**: Example script to run the Python CLI (`python3 -m xprt_commit.main`).

## devDependencies

- **lint-staged**: Lints only staged files before commit.
- **lefthook**: Manages git hooks (pre-commit, commit-msg, etc).

## files

- Controls which files are included when publishing the package.

## repository, bugs

- Links to the GitHub repository and issues page for support.

## license

- Specifies the license for open source compliance.

---

## Notes

- Add a `"main"` or `"exports"` field if you provide a JS/TS entry point for importability.
- Adjust scripts and dependencies to match your actual project (e.g., add `eslint`, `prettier`, `black` as needed).
- See `lint-staged.config.js` and `lefthook.yml` for staged linting and hook management.
