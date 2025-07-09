# Project Conventions

## Overview

- This document has the purpose of defining the CONVENTIONS, PRINCIPLES & STRUCTURES for the project: {{}}.
- Additionally, detailed are a set of guidelines and best practices for the project: {{}} .

## 1. Documentation Law

- **Purpose:**
    * Documentation will be generated to provide context to AI Agents & Aid Human understanding.
    * Create logs that enable work to be resumed, even with a fresh context & to preserve a historical record of work.
- **Agent Context:**
    * Structure documentation efficiently
    * Use clear heading, concise summaries, and relevant references.
- **Readability:**
    * Name files with clarity of their purpose in mind
    * Employ consistency in naming & formatting conventions
    * Use Diagrams & Emojis to optimize understanding
- **Granularity:**
    * Create log files specific to a particular task in `project_journal/tasks`
    * Name log files and task files with sequential numbering: e.g., `001_monorepo_setup.md`
- **Centrality:**
    * Group related information in a logical organization

## 2. Structure Standardization

The below are presented as: directory/ -> naming convention -> description

- `tasks/`:
    * `TASK-ID.md`
    * Log detailed history -> goals, steps, findings, outcomes -> for individual tasks
- `decisions/`:
    * `YYYYMMDD_topic.md`
    * Document significant, project level scope decisions like an ADR
- `formal_docs/`:
    * `NNN-doc_name.md`
    * Final outputs -> reports, specs, guides, research, audits, test plans, configs
- `visualizations/`:
    * `TYPE-diagram_name.md`
    * Diagrams -> architecture, DB, Schema, Task Status, Workflows
    * e.g., `ARCH-system_context.md`, `DB-postgreSQL.md`
- `planning/`:
    * `TYPE-doc_name.md`
    * Core planning documents -> `PRD-requirements.md`, `ARCH-architecture.md`, `PROJ-project_plan.md`
- `technical_notes/`:
    * `NNN-note_name.md`
    * For ad-hoc technical documentation not in any of the above categories

## 3. Standardized Emoji Legend

Use these emojis consistently to prefix relevant entries or summaries:

- 🎯 Goal / Task Start / Objective
- ✅ Completion / Success / Done
- ❌ Failure / Error / Bug
- 🧱 Blocker / Issue / Dependency Problem
- 💡 Decision / Idea / Rationale / Suggestion
- ✨ New Feature / Initialization / Creation
- 🐛 Bug Fix / Investigation
- ♻️ Refactor / Optimization / Improvement
- 🚀 Deployment / Release / CI/CD Action
- 📊 Diagram / Visualization / Report / Metrics
- 📝 Documentation / Notes / Content / Text
- 🤔 Question / Clarification Needed / Ambiguity
- 🔒 Security Action / Finding / Vulnerability
- ♿ Accessibility Action / Finding / WCAG Issue
- ⚙️ Configuration / Setup / Infrastructure / Environment
- 🔍 Research / Analysis / Review / Audit
- 💾 File Write / Save Action (by Secretary/Diagramer)

## 4. General Delegation Guidelines (via `new_task`)

- **Task ID:** Always include the relevant Task ID in the delegation message.
- **Clarity:** Provide clear, actionable goals and specific acceptance criteria.
- **Context:** Reference necessary context files (e.g., `project_journal/planning/requirements.md#section-3`, `project_journal/tasks/TASK-ABC.md`) or previous Task IDs.
- **Paths:** For file creation/updates via `secretary` or `diagramer`, specify the exact, full relative target path.

## 5. File Management

- **Code:** Modes responsible for specific code types (e.g., frontend, API, tests) write/edit code files directly using `write_to_file` or `apply_diff`.
- **Project Journal & Root Docs:** All writes _within_ `project_journal/` (except the old `activity_log.md`) and to root `README.md`/`LICENSE.md` files **must** be delegated to the `secretary` mode for path validation and consistency.
- **Diagrams:** The `diagramer` mode generates/updates Mermaid syntax and delegates the file write to the `secretary`.

## 6. Practices

- ✅ Ensure there is a clear and consistent approach to
  - coding
  - documentation
  - project structure.
- ✅ Ensure there is a single source of truth for which package management tools to use.
- ✅ Ensure:
    * All parts of the project are documented
    * All code is linted and formatted
    * All code is tested

## 7. Language Rules

### JavaScript, Typescript, & Node.js

- ❌ DO NOT use
  - `npm`
  - `yarn`
- ✅ ALWAYS use
  - `pnpm`

### Python

- ❌ DO NOT use
  - `pip`
  - `poetry`
  - `venv`
  - `pipenv`
  - `conda`
  - `virtualenv`
  - `pyenv`
- ✅ ALWAYS use
  - `pdm`
  - `uv`
  - For example `pdm list`
-􀩼- Add a python package to the `pyproject.toml` file with `pdm add <package-name>`
- - Python packages and apps are created with the commands:
      * `pdm init`
      * `source .venv/bin/activate`

### Turborepo
When a project is a monorepo implemented with:
- Turborepo [Turborepo](https://turborepo.org/).

    * Then this Turborepo uses [pnpm](https://pnpm.io/) for package management.
    * & this Turborepo uses [turbo](https://turbo.build/) for task management.
    * When possible and appropriate add task commands to the `turbo.json` file.

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

## 8. Coding

- 📝 Before writing any code, first write a plan.
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
- When a task is completed write an update in the relevant Task file in the `/project_journal/tasks/` directory
- If a significant decision is made, write an entry in the `/project_journal/decisions` directory.
