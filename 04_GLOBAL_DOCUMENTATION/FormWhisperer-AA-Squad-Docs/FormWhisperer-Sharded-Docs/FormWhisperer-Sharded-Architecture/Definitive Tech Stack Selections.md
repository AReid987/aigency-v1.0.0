---
type: Page
title: Definitive Tech Stack Selections
description: null
icon: null
createdAt: '2025-07-11T08:43:13.062Z'
creationDate: 2025-07-11 03:43
modificationDate: 2025-07-11 03:47
tags: []
coverImage: null
---

#### `docs/tech-stack.md`

# Definitive Tech Stack Selections

This section outlines the definitive technology choices for the project. These selections should be made after a thorough understanding of the project's requirements, components, data models, and core workflows. The Architect Agent should guide the user through these decisions, ensuring each choice is justified and recorded accurately in the table below.
This table is the **single source of truth** for all technology selections. Other architecture documents (e.g., Frontend Architecture) must refer to these choices and elaborate on their specific application rather than re-defining them.
Key decisions to discuss and finalize here, which will then be expanded upon and formally documented in the detailed stack table below, include considerations such as:

- Preferred Starter Template Frontend: { Url to template or starter, if used }

- Preferred Starter Template Backend: { Url to template or starter, if used }

- Primary Language(s) & Version(s): {e.g., TypeScript 5.x, Python 3.11 - Specify exact versions, e.g., `5.2.3`}

- Primary Runtime(s) & Version(s): {e.g., Node.js 22.x - Specify exact versions, e.g., 22.0.1}

- Must be definitive selections; do not list open-ended choices (e.g., for web scraping, pick one tool, not two). 

- Specify exact versions (e.g., 18.2.0). If 'Latest' is used, it implies the latest stable version at the time of this document's last update, and the specific version (e.g., xyz-library@2.3.4) should be recorded. 

- Pinning versions is strongly preferred to avoid unexpected breaking changes for the AI agent.

| Category         | Technology                        | Version / Details                        | Description / Purpose                                                                     | Justification (Optional)                                                                          |
| :--------------- | :-------------------------------- | :--------------------------------------- | :---------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------ |
| Languages        | TypeScript                        | 5.x                                      | Primary language for Node.js backend services and web frontend.                           | Strong typing, large ecosystem, good for complex service orchestration.                           |
|                  | Python                            | 3.11                                     | Used for AI/ML components (persona modeling, response generation) and browser automation. | Rich AI/ML libraries, strong scripting capabilities for automation.                               |
| Runtime          | Node.js                           | 22.x                                     | Server-side execution environment for orchestrator and other backend services.            | High performance for I/O bound tasks, large package ecosystem.                                    |
| Frameworks       | NestJS / Express.js               | Latest (e.g., NestJS 10.x / Express 4.x) | Backend API framework for persona, HITL, and automation orchestrator services.            | NestJS for structured, enterprise-grade applications; Express for simplicity in smaller services. |
|                  | FastAPI                           | Latest (e.g., 0.111.x)                   | Python web framework for AI/automation services, known for performance and type hints.    | High performance, automatic OpenAPI documentation, good for data-intensive APIs.                  |
|                  | React                             | Latest (e.g., 18.x)                      | Frontend UI library for persona setup/management.                                         | Component-based, large community, suitable for dynamic UIs.                                       |
|                  | Next.js                           | Latest (e.g., 14.x)                      | React framework for web UI (SSR, routing).                                                | Provides full-stack capabilities, server-side rendering for performance.                          |
| Databases        | MongoDB                           | 7.0                                      | Primary NoSQL data store for flexible persona data and survey completion records.         | Schema flexibility suits varied persona attributes and evolving survey data.                      |
| Cloud Platform   | AWS                               | N/A                                      | Primary cloud provider for hosting all services.                                          | Comprehensive suite of services, scalability, reliability.                                        |
| Cloud Services   | AWS Lambda                        | N/A                                      | Serverless compute for stateless backend functions (e.g., HITL trigger).                  | Cost-effective, scales automatically.                                                             |
|                  | AWS S3                            | N/A                                      | Object storage for static assets (e.g., frontend build artifacts).                        | Highly durable, scalable, cost-effective storage.                                                 |
|                  | AWS DynamoDB                      | N/A                                      | (Consider for high-performance, key-value data, e.g., session state for agents).          | High performance, fully managed NoSQL for specific high-throughput needs.                         |
| Infrastructure   | AWS CDK                           | Latest                                   | Infrastructure as Code (IaC) tool for defining and provisioning AWS resources.            | Uses familiar programming languages, good for complex cloud setups.                               |
|                  | Docker                            | Latest                                   | Containerization for deploying services consistently across environments.                 | Portability, isolation, consistent runtime.                                                       |
| UI Libraries     | Tailwind CSS                      | Latest (e.g., 3.x)                       | Utility-first CSS framework for rapid UI styling.                                         | Highly customizable, efficient for reactive design.                                               |
| State Management | Zustand                           | Latest (e.g., 4.x)                       | Frontend state management for the web UI.                                                 | Simple, fast, and scalable for React applications.                                                |
| Testing          | Jest                              | Latest (e.g., 29.x)                      | Unit/Integration testing framework for Node.js (TypeScript) and React.                    | Widely adopted, good for mocking, snapshot testing.                                               |
|                  | Playwright                        | Latest (e.g., 1.44.x)                    | End-to-end testing framework for browser automation.                                      | Supports multiple browsers, strong for E2E tests, can run alongside Browser Use/MCP.              |
|                  | Pytest                            | Latest (e.g., 8.x)                       | Unit/Integration testing framework for Python agents.                                     | Simple, extensible, widely used in Python community.                                              |
| CI/CD            | GitHub Actions                    | N/A                                      | Continuous Integration/Deployment pipeline automation.                                    | Integrated with GitHub, flexible workflows.                                                       |
| Other Tools      | LangChain.js / LangChain (Python) | Latest                                   | Library for integrating LLMs and orchestrating complex AI workflows.                      | Facilitates interaction with LLMs, prompt engineering.                                            |
|                  | Browser Use                       | Latest                                   | Primary framework for robust browser automation and interaction.                          | Specified by user for performance and reliability.                                                |
|                  | Browser MCP                       | Latest                                   | Alternative/complementary framework for high-performance browser automation.              | Specified by user for advanced automation needs.                                                  |
