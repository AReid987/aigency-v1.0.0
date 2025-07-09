# Project Backlog

This document outlines the project backlog, organized by Epics. Each task within an Epic includes a complexity score (1-10) used for tracking project completion percentage.

## Epics

### Epic 1: Core Functionality

- **Description:** Implement the fundamental features required for the application to be functional.

#### Tasks

- [x] Task: User Authentication (Complexity: 5) - FastAPI endpoints with Supabase Auth (local) complete.
- [x] Task: Basic Data Storage (Complexity: 6) - Core schema defined, Supabase local DB reset & migrations applied.
- [x] Task: User Interface Framework Setup (Complexity: 4) - Basic Next.js structure, layout, and placeholder Login/Signup forms at `/auth` route are functional.
- [ ] Task: Implement Custom Auth Form UI (based on 21st.dev example, XPRT branding, Radix UI) (Complexity: 5)
- [ ] Task: Add visual feedback (e.g., loading state) to login/signup form submit buttons (Complexity: 3)
- [ ] Task: Implement email confirmation flow for new user sign-ups (Complexity: 5)
- [ ] Task: Design and implement micro-interactions for successful login/signup (Complexity: 3)
- [ ] Task: Design and implement micro-interactions for unsuccessful login/signup attempts (Complexity: 3)
- [ ] Task: Implement client-side and server-side form field validation for auth forms (email format, password strength, required fields) (Complexity: 5)

### Epic 2: Advanced Features

- **Description:** Develop additional features that enhance the application's capabilities.

#### Tasks

- [x] Task: Implement Search Functionality (API Structure & DB) (Complexity: 4 of 7) - FastAPI endpoint for search created, authenticates user, stores placeholder results in DB linked to `auth.users`.
  - [ ] Sub-Task: Integrate Brave Search MCP Tool into Search API (Complexity: 3 of 7)
- [ ] Task: Add User Profiles (Complexity: 5)
- [ ] Task: Develop Reporting Module (Complexity: 8)
- [ ] Task: Implement Mem0 for user personalization
  - Enable Agents to determine and remember User Preferences & Habits
  - Share long term memory across agents, sessions, even between team mates (Complexity: 7)

### Epic 3: Polish and Optimization

- **Description:** Focus on improving performance, usability, and overall quality.

#### Tasks

- [ ] Task: Optimize Database Queries (Complexity: 6)
- [ ] Task: Improve UI Responsiveness (Complexity: 5)
- [ ] Task: Write Unit Tests (Complexity: 7)

### Epic 4: Infrastructure and Data Operations

- **Description:** Establish robust infrastructure, CI/CD pipelines, and data ingestion/processing strategies.

#### Tasks

- [ ] Task: Containerization Strategy (Complexity: 7) - Define and create images/containers for each microservice.
- [ ] Task: DevSecOps Pipeline (Complexity: 8) - Create CI/CD pipeline for automated updates, validation, image maintenance, and local cleanup.
- [ ] Task: UX Feature - Custom Dashboard (Complexity: 6) - Design and implement a custom dashboard for feeds (e.g., using Perses).
- [ ] Task: Functional Requirement - Web Scraping Integration (Complexity: 7) - Implement Crawl4AI & LightRAG to scrape content after web searches.
- [ ] Task: ETL Strategy for Content Ingestion (Complexity: 8) - Research and plan autonomous ETL strategies for uploaded and scraped content.
- [ ] Task: Implement BrainCraft (Complexity: 9) - Integrate and refactor local BrainCraft repo.
  - [ ] Sub-Task: Refactor BrainCraft to use Crawl4AI instead of ScrapeGraph (Complexity: 4)
  - [ ] Sub-Task: Refactor BrainCraft to use a FOSS LLM instead of OpenAI (Complexity: 5)

---

### Epic: Design System &amp; UI Consistency

**Description:** Establish and enforce consistent design principles and UI patterns across the application.

**Tasks:**

- [ ] Task: Implement 8px Grid System (Complexity: 6) - All UI layouts, components, and elements should be sized and spaced based on an 8px grid.
- [ ] Task: Implement Systematic Design System generation via conversational interface (Complexity: 9)

### Epic: Idea Validation & Strategy Platform

- **Description:** Develop a platform for validating startup/product/feature ideas using conversational AI and research.

#### Tasks

- [ ] Task: Implement conversational interface for idea submission and discussion with XPRT agent team (Complexity: 8)
- [ ] Task: Integrate research-based validation using web search / deep research enabled agents (Complexity: 9)
- [ ] Task: Develop a logical framework for validating idea potential (Complexity: 7)
- [ ] Task: Create a standardized scoring system for ideas (Complexity: 6)
- [ ] Task: Implement proactive suggestions & metrics for measurement (Complexity: 7)
- [ ] Task: Develop success strategy generation capabilities (Complexity: 8)

### Epic: AI/LLM Operations & Development

- **Description:** Tools and infrastructure for managing and improving AI/LLM components.

#### Tasks

- [ ] Task: Implement prompt engineering & evaluation dashboard (Complexity: 8)
- [ ] Task: Implement AI Gateway for managing model access (Complexity: 7)
- [ ] Task: Implement Crawl4AI + LightRAG for research, ingest, ETL automation (Complexity: 8)
  - [ ] Sub-Task: Develop HITL workflow for approving ingested content from web searches.

### Epic: Development Tooling & Workflow

- **Description:** Enhancements and integrations for the development lifecycle.

#### Tasks

- [ ] Task: Finish and implement CommitZen (Complexity: 6)

### Epic: Public Website & Marketing

- **Description:** Development and enhancement of the public-facing landing page and marketing materials.

#### Tasks

- [ ] Task: Finish Landing Page (Complexity: 7)
  - [ ] Sub-Task: Add/Update Features section.
  - [ ] Sub-Task: Incorporate Social Proof.
  - [ ] Sub-Task: Increase Robustness of Call to Actions (CTAs).

### Epic: Observability & Monitoring

- **Description:** Implement comprehensive monitoring for application performance, user behavior, and AI/LLM operations.

#### Tasks

- [ ] Task: Implement Application Performance Monitoring (e.g., Grafana, Prometheus) (Complexity: 7)
- [ ] Task: Implement User Behavior Monitoring (e.g., Hotjar, PostHog) (Complexity: 6)
- [ ] Task: Implement LLM & Agent Monitoring (e.g., LLMetry, Langflow, AgentOps) (Complexity: 8)
- [ ] Task: Implement Prompt Engineering Monitoring/Management (e.g., Portkey, Promptfoo, Opik) (Complexity: 7)

---

- [ ] Fix Next.js startup issue
- [ ] Create devcontainer setup for the repository (IDE, extensions, etc.)
