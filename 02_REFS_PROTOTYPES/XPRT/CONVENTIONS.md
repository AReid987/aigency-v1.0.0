# XPRT Conventions

## Overview

- This Conventions file provides a set of guidelines and best practices for the devLog XPRT project.

## Purpose

### These conventions ensure that

- There is a clear and consistent approach to
  - coding
  - documentation
  - project structure.
- There is a single source of truth for which package management tools to use.
- All parts of the project are documented
- All code is linted and formatted
- All code is tested

## Use Cases

- These conventions are ideal for the following use cases:
  - Coding
  - Documentation
  - Testing

## Usage

### JavaScript, Typescript, & Node.js

- DO NOT use
  - `npm`
  - `yarn`
- ALWAYS use
  - `pnpm`

### Python

- DO NOT use
  - `pip`
  - `poetry`
  - `venv`
  - `pipenv`
  - `conda`
  - `virtualenv`
  - `pyenv`
- ALWAYS use
  - `pdm`
  - `uv`
  - For example `pdm list`
- Add a python package to the `pyproject.toml` file with `pdm add <package-name>`
- Python packages and apps are created with the commands:
  - `pdm init`
  - `source .venv/bin/activate`

### Turborepo

- This is a monorepo managed by [Turborepo](https://turborepo.org/).
- This Turborepo uses [pnpm](https://pnpm.io/) for package management.
- This Turborepo uses [turbo](https://turbo.build/) for task management.
- When possible and appropriate add task commands to the `turbo.json` file.

#### Apps & Packages

- Standalone code is created as an app in the `apps` directory.
- Shared code is created as a package in the `packages` directory.
- Apps and packages have a package.json file.
  - Create a package.json file for each app and package with `pnpm init`.
  - The package.json file should have the field `"name"` set to the name of the app or package with `@xprt/` prefix.
  - The package.json file should have the field `"version"` set to "0.0.0".
- Apps and packages have a README.md file.
  - The README.md file should
    - give a high level overview of the app or package.
    - include installation instructions, usage instructions, and any other relevant information.

## Coding

- Before writing any code, first write a plan.
- Plans can be added to the `/project_journal/planning` directory
- After writing a plan, break the plan into smaller tasks.
- Tasks can be added to the `/project_journal/backlog.md` file
- Backlogs consist of Epics, Stories, and Tasks.
- Epics are made up of stories and Tasks
- Tasks should each be given a complexity score 1 - 10
- When implementing
  - For each task, first write a test.
  - After writing a test, write the code.
  - After writing the code, run the test.
  - After running the test, fix any errors.
  - After fixing any errors, run the test again.
  - Continue running the test and fixing any errors until the test passes.
  - When the test passes, commit the code.
- Repeat the process for each task.
- When a task is completed write an entry in the `/project_journal/progress/progress_log.md` file.
- If a significant decision is made, write an entry in the `/project_journal/decisions` directory.
