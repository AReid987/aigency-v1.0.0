---
type: Page
title: Operational Guidelines
description: null
icon: null
createdAt: '2025-07-11T08:48:09.847Z'
creationDate: 2025-07-11 03:48
modificationDate: 2025-07-11 03:48
tags: []
coverImage: null
---

# Operational Guidelines

### Error Handling Strategy

- **General Approach:** Exceptions will be the primary mechanism for signaling errors within services. Custom error types will be defined for domain-specific business logic errors. APIs will return standardized JSON error responses with clear status codes.

- **Logging:**

    - **Library/Method:** For Node.js, `Pino` for structured logging. For Python, `structlog` with `python-json-logger`.

    - **Format:** JSON for all logs to facilitate centralized logging and analysis.

    - **Levels:** DEBUG, INFO, WARN, ERROR, CRITICAL. Standard usage will be defined.

    - **Context:** All logs must include `correlationId` (for tracing requests across services), `serviceName`, `operationName`, and sanitized `userId` (if applicable). Sensitive PII must never be logged.

- **Specific Handling Patterns:**

    - **External API Calls:** `axios-retry` (TypeScript) and `tenacity` (Python) for retry mechanisms with exponential backoff and max retries (e.g., 3 retries). Timeouts (connect and read) will be strictly enforced. Circuit breaker patterns (e.g., using `opossum` in Node.js) will be considered for critical external services. 4xx client errors will be propagated, 5xx server errors will trigger retries or specific alerts.

    - **Internal Errors / Business Logic Exceptions:** Custom error classes inheriting from a base `AppError` (TypeScript) or `AppException` (Python) will be used. User-facing errors will provide generic messages with a unique error ID for support, avoiding sensitive information leakage.

    - **Transaction Management:** Given MongoDB, transactional capabilities will be used for multi-document operations to ensure data consistency.

### Coding Standards

These standards are mandatory for all code generation by AI agents and human developers. Deviations are not permitted unless explicitly approved and documented as an exception in this section or a linked addendum.

- **Primary Runtime(s):** Node.js 22.x, Python 3.11

- **Style Guide & Linter:**

    - **TypeScript/Node.js:** ESLint with Airbnb config + Prettier. Configuration files: `.eslintrc.js`, `.prettierrc`.

    - **Python:** Black for formatting, Flake8 for linting, MyPy for type checking. Configuration files: `pyproject.toml`.

    - Linter rules are mandatory and must not be disabled without cause.

- **Naming Conventions:**

    - Variables: `camelCase` (TypeScript/JavaScript), `snake_case` (Python).

    - Functions/Methods: `camelCase` (TypeScript/JavaScript), `snake_case` (Python).

    - Classes/Types/Interfaces: `PascalCase`.

    - Constants: `UPPER_SNAKE_CASE`.

    - Files: `kebab-case.ts` (TypeScript), `snake_case.py` (Python), `PascalCase.tsx` (React components).

    - Modules/Packages: `camelCase` (TypeScript/JavaScript), `snake_case` (Python).

- **File Structure:** Adhere to the monorepo layout defined in the Project Structure.

- **Unit Test File Organization:**

    - **TypeScript/Node.js:** `*.test.ts` or `*.spec.ts` co-located with source files (e.g., `src/services/persona-service/src/index.test.ts`).

    - **Python:** `test_*.py` in a parallel `test/unit/` directory mirroring the `src/agents/` structure (e.g., `test/unit/agents/browser-automator/test_main.py`).

- **Asynchronous Operations:** Always use `async`/`await` for promise-based operations (TypeScript/Python).

- **Type Safety:**

    - **TypeScript:** Strict mode (all flags enabled) in `tsconfig.json`. Avoid `!` non-null assertion operator; prefer explicit checks, optional chaining (`?.`), or nullish coalescing (`??`).

    - **Python:** All new functions and methods must have full type hints. MyPy will be enforced in CI.

    - **Type Definitions:** Global types in `src/shared/types/`. Policy on using `any` or equivalent is strongly discouraged and requires justification.

- **Comments & Documentation:**

    - Code Comments: Explain *why*, not *what*, for complex logic. Use JSDoc (TypeScript), Python docstrings (Google style).

    - READMEs: Each `src/services/` and `src/agents/` module will have a README.md.

- **Dependency Management:** `npm`/`yarn` workspaces for Node.js, Poetry/Pipenv for Python. Prefer pinned versions for stability. New dependencies require security scans and approval.

### Overall Testing Strategy

This section outlines the project's comprehensive testing strategy, which all AI-generated and human-written code must adhere to.

- **Tools:** Jest, Playwright, Pytest.

- **Unit Tests:**

    - **Scope:** Test individual functions, methods, classes, or small modules in isolation. Focus on business logic, algorithms, and data transformations.

    - **Location:**

        - **TypeScript/Node.js:** `*.test.ts` or `*.spec.ts` co-located with source files.

        - **Python:** `test_*.py` in a parallel `test/unit/` directory mirroring the `src/agents/` structure.

    - **Mocking/Stubbing:** Jest mocks (TS), `unittest.mock` (Python). Mock all external dependencies (network, file system, databases, LLM APIs).

    - **AI Agent Responsibility:** AI Agent must generate unit tests covering all public methods, significant logic paths, edge cases, and error conditions for any new or modified code.

- **Integration Tests:**

    - **Scope:** Test interaction between several components or services (e.g., `Automation Orchestrator` to `Persona Service`, `Response Generator` to `LLM`).

    - **Location:** `test/integration/` mirroring the `src/` structure.

    - **Environment:** Testcontainers for databases/external services (if needed), in-memory databases, or dedicated test environments.

    - **AI Agent Responsibility:** AI Agent may generate integration tests for key service interactions or internal API endpoints.

- **End-to-End (E2E) Tests:**

    - **Scope:** Validate complete user flows or critical paths through the system from the user's perspective, specifically for survey completion. Example flows: "Successful completion of a multi-page survey," "Triggering and resolving an HITL scenario," "Persona setup and subsequent survey completion."

    - **Tools:** Playwright.

    - **AI Agent Responsibility:** AI Agent may generate E2E test stubs or scripts based on user stories or BDD scenarios, focusing on critical happy paths and key error scenarios.

- **Test Coverage:** Target 80% line/branch coverage for unit tests (guideline).

- **Mocking/Stubbing Strategy (General):** Prefer fakes or test doubles over extensive mocking when it improves clarity. Strive for fast, reliable, isolated tests.

- **Test Data Management:** Factories and fixtures for test data creation. Setup/teardown scripts for isolation.

### Security Best Practices

- **Input Sanitization/Validation:** All external inputs (API requests, user-provided data, form fields from surveys) must be sanitized and validated using `class-validator` with DTOs (TypeScript) or Pydantic (Python). Validation must occur at the service boundary.

- **Output Encoding:** React's JSX auto-escaping will be relied upon for frontend. For backend-generated content, use contextually appropriate encoding libraries (e.g., `html-entities` for HTML, JSON stringify for JSON) to prevent XSS.

- **Secrets Management:** Environment variables (`.env`, AWS Secrets Manager) for all secrets (API keys, database credentials, bot tokens). Never hardcode secrets or commit them to source control. Access via a designated configuration module/service.

- **Dependency Security:** Automated vulnerability scans (`npm audit`, `pip-audit`, Snyk, Dependabot) in CI. High/critical vulnerabilities addressed promptly.

- **Authentication/Authorization Checks:** All internal service APIs (except explicitly public ones) must enforce authentication/authorization using internal API keys or short-lived JWTs. The `Persona Service` and `HITL Orchestration Service` will have strict access controls.

- **Principle of Least Privilege (Implementation):** Database users will have minimal necessary permissions. AWS IAM roles will be narrowly scoped to specific actions and resources for each service.

- **API Security (General):** Enforce HTTPS for all communication. Implement rate limiting and throttling on exposed APIs. Use standard HTTP security headers (CSP, HSTS).

- **Error Handling & Information Disclosure:** Error messages must not leak sensitive information (stack traces, internal paths) to clients. Log detailed errors server-side, provide generic messages or error IDs to the client.

- **Regular Security Audits/Testing:** SAST/DAST tools integrated into CI.

