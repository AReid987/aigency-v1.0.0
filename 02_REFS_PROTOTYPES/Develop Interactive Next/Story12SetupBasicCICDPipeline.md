---
type: Page
collections: sportsclub backlog
title: 'Story 1.2: Set up Basic CI/CD Pipeline'
description: null
icon: null
createdAt: '2025-06-06T09:30:54.74Z'
creationDate: 2025-06-06 04:30
modificationDate: 2025-06-11 23:10
tags: [Story]
coverImage: null
---

# Story 1.2: Set up Basic CI/CD Pipeline

# Status: Draft

## Story

- As a **developer**,

- I want to **set up a basic Continuous Integration/Continuous Deployment (CI/CD) pipeline for the monorepo**,

- so that **automated builds and initial code quality checks are performed, enabling continuous integration and early feedback on changes**.

## Acceptance Criteria (ACs)

1. A CI/CD workflow file (e.g., `.github/workflows/main.yml` if using GitHub Actions) is created in the project root.

2. The pipeline is configured to trigger on pushes to the `main` branch and pull requests.

3. The pipeline successfully checks out the monorepo code.

4. The pipeline installs project dependencies using the defined package managers (PNPM for JS/TS, PDM/uv for Python).

5. The pipeline includes steps to run `Turborepo` builds for all monorepo packages (e.g., `web`, `auth-service`).

6. The pipeline includes basic linting/formatting checks for both frontend (Next.js/TS) and backend (FastAPI/Python) codebases, failing the build if errors are found.

7. The pipeline successfully completes without errors on a test commit/PR.

## Tasks / Subtasks

- [ ] Create initial CI/CD workflow file (e.g., for GitHub Actions).

- [ ] Configure workflow triggers for pushes to `main` and pull requests.

- [ ] Add steps to checkout code.

- [ ] Add steps to set up Node.js and Python environments.

- [ ] Add steps to install root monorepo dependencies (PNPM, PDM/uv).

- [ ] Add steps to run `Turborepo` build command for all packages.

- [ ] Add linting/formatting steps for TypeScript/JavaScript (ESLint, Prettier).

- [ ] Add linting/formatting steps for Python (Black, Flake8).

- [ ] Test pipeline with a dummy commit/PR to verify successful execution.

## Dev Technical Guidance

This story focuses on establishing the initial automated pipeline for continuous integration. It is critical for early feedback on code quality and build health.

- **CI/CD Tool:** GitHub Actions is the chosen CI/CD tool. Refer to GitHub Actions documentation for workflow syntax.

- **Monorepo Integration:** The pipeline must correctly utilize `Turborepo` commands (`turbo run build`, `turbo run lint`) to operate efficiently across workspaces.

- **Dependency Installation:** Ensure `PNPM` and `PDM/uv` are correctly used for dependency installation within the CI environment.

- **Linting:** Configure ESLint/Prettier for Next.js and Black/Flake8 for FastAPI. Refer to the "Coding Standards" section in the Architecture Document for specific tools and preferences.

- **Build Steps:** The pipeline should invoke `turbo run build` to ensure all packages can be built.

- **Verification:** Confirm pipeline runs successfully on push/PR, indicating successful build and linting.

## Story Progress Notes

### Agent Model Used: Bob (SM Agent)

### Completion Notes List

- (To be filled by Developer Agent upon completion)

### Change Log

- (To be filled by Developer Agent upon completion)

