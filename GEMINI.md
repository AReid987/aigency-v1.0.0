# Project Overview

This project is a Turborepo monorepo, primarily focused on developing "KnowledgeWeaver," an advanced, AI-driven knowledge engineering platform. KnowledgeWeaver aims to autonomously transform unstructured web content into structured, queryable, and dynamically evolving knowledge bases. It leverages cutting-edge open-source innovations for intelligent web crawling, multimodal data extraction, autonomous ETL, and the creation of sophisticated vector databases and neural knowledge graphs. The monorepo also contains other applications and packages, including Next.js apps, React component libraries, and configurations for ESLint and TypeScript.

# Building and Running

The project uses `pnpm` as its package manager and `Turborepo` for monorepo management.

*   **Install Dependencies:**
    ```bash
    pnpm install
    ```
*   **Build all apps and packages:**
    ```bash
    pnpm exec turbo build
    ```
    To build a specific package (e.g., `docs`):
    ```bash
    pnpm exec turbo build --filter=docs
    ```
*   **Develop all apps and packages:**
    ```bash
    pnpm exec turbo dev
    ```
    To develop a specific package (e.g., `web`):
    ```bash
    pnpm exec turbo dev --filter=web
    ```
*   **Run specific development scripts:**
    *   For `apps/extract`:
        ```bash
        cd apps/extract && pdm run dev
        ```
    *   For `apps/survey-automation`:
        ```bash
        cd apps/survey-automation && pdm run dev
        ```
    *   For `apps/survey-automation` with Docker:
        ```bash
        docker-compose -f docker-compose.survey.yml up --build
        ```
    *   For `tui:extract`:
        ```bash
        cd apps/extract && .venv/bin/python run_tui.py
        ```
*   **Lint code:**
    ```bash
    pnpm exec turbo lint
    ```
*   **Format code:**
    ```bash
    prettier --write "**/*.{ts,tsx,md}"
    ```
*   **Check types:**
    ```bash
    pnpm exec turbo check-types
    ```

# Development Conventions

*   **Language:** Primarily TypeScript for web applications and configurations. Python is used for specific applications like `apps/extract` and `KnowledgeWeaver`.
*   **Monorepo Tool:** Turborepo is used for managing the monorepo, enabling efficient task running and caching across packages.
*   **Package Manager:** `pnpm` is the preferred package manager.
*   **Linting:** ESLint is configured for code linting.
*   **Formatting:** Prettier is used for consistent code formatting.
*   **Type Checking:** TypeScript is used for static type checking.
*   **Product Planning:** The project follows a structured product planning process, with documentation stored in `.agent-os/product/` (versioned as `planning-v1` and `planning-v2`).