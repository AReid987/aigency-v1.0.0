---
type: Page
title: Project Structure
description: null
icon: null
createdAt: '2025-07-11T08:41:18.448Z'
creationDate: 2025-07-11 03:41
modificationDate: 2025-07-11 03:41
tags: []
coverImage: null
---

# Project Structure

## Project Structure

{Provide an ASCII or Mermaid diagram representing the project's folder structure. The following is a general example. If a `front-end-architecture-tmpl.txt` (or equivalent) is in use, it will contain the detailed structure for the frontend portion (e.g., within `src/frontend/` or a dedicated `frontend/` root directory). Shared code structure (e.g., in a `packages/` directory for a monorepo) should also be detailed here.}

```markdown
FormWhisperer/
├── .github/                    # CI/CD workflows
│   └── workflows/
│       └── main.yml
├── .vscode/                    # VSCode settings (optional)
│   └── settings.json
├── build/                      # Compiled output (often git-ignored)
├── config/                     # Static configuration files
├── docs/                       # Project documentation (PRD, Arch, UI/UX Spec, etc.)
│   ├── architecture.md         # This document
│   ├── prd.md                  # Product Requirements Document
│   ├── front-end-spec.md       # UI/UX Specification
│   ├── environment-vars.md     # Specific environment variable definitions
│   ├── data-models.md          # Detailed data schemas
│   ├── api-reference.md        # External/internal API definitions
│   ├── project-structure.md    # Detailed project folder structure
│   ├── tech-stack.md           # Definitive technology selections
│   ├── operational-guidelines.md # Coding standards, testing, error handling, security
│   ├── component-view.md       # Detailed component breakdown
│   ├── sequence-diagrams.md    # Core workflow diagrams
│   ├── infra-deployment.md     # Infrastructure & deployment overview
│   └── key-references.md       # Links to other important documents
├── node_modules/               # Project dependencies (git-ignored)
├── scripts/                    # Utility scripts (e.g., build, deploy, test runners)
├── src/                        # Application source code (Monorepo root)
│   ├── services/               # Node.js/TypeScript backend services
│   │   ├── persona-service/    # Persona CRUD logic
│   │   │   └── src/
│   │   ├── hitl-service/       # HITL communication logic
│   │   │   └── src/
│   │   └── automation-orchestrator/ # Main orchestration logic
│   │       └── src/
│   ├── agents/                 # Python AI/automation components
│   │   ├── browser-automator/  # Browser control logic
│   │   │   └── src/
│   │   ├── form-parser/        # Form element identification
│   │   │   └── src/
│   │   ├── response-generator/ # LLM interaction and persona logic
│   │   │   └── src/
│   │   └── shared-python/      # Common Python utilities/models
│   ├── shared/                 # Shared TypeScript types, utilities (used by Node.js and frontend)
│   │   └── types/
│   └── web-ui/                 # React/Next.js Frontend (optional MVP)
│       ├── public/
│       ├── src/
│       └── ...
├── test/                       # Automated tests (unit, integration, e2e)
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore rules
├── package.json                # Monorepo root package.json (npm/yarn workspaces)
├── tsconfig.json               # TypeScript configuration
├── pyproject.toml              # Python project configuration (Poetry/Pipenv)
├── Dockerfile                  # Docker build instructions (if applicable)
└── README.md                   # Project overview and setup instructions
```

