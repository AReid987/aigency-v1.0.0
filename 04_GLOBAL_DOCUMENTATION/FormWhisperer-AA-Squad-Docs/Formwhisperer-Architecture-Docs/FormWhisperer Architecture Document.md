---
type: Page
title: FormWhisperer Architecture Document
description: null
icon: null
createdAt: '2025-07-11T07:11:35.804Z'
creationDate: 2025-07-11 02:11
modificationDate: 2025-07-11 03:18
tags: []
coverImage: null
---

# FormWhisperer Architecture Document

## Introduction / Preamble

This document outlines the overall project architecture for FormWhisperer, including backend systems, shared services, and non-UI specific concerns. Its primary goal is to serve as the guiding architectural blueprint for AI-driven development, ensuring consistency and adherence to chosen patterns and technologies.

**Relationship to Frontend Architecture:** FormWhisperer includes a significant user interface for persona setup and Human-in-the-Loop (HITL) interactions. A separate UI/UX Specification (`docs/front-end-spec.md`) has been created, and a Frontend Architecture Document (to be named `docs/front-end-architecture.md`) will detail the frontend-specific design. This main architecture document must be used in conjunction with those, as core technology stack choices documented herein are definitive for the entire project.

## Table of Contents

{ Update this if sections and subsections are added or removed }

## Technical Summary

FormWhisperer will be built as a **Monorepo** containing distinct services: a core AI agent for browser automation and persona-driven response generation, an HITL orchestration service, and a lightweight web UI for persona setup. The architecture leverages Node.js with Express/NestJS for backend services and Python with FastAPI for AI/automation components. Browser automation will utilize 'Browser Use' and 'Browser MCP'. Data will be stored in a NoSQL database. The system emphasizes realistic human-like interaction and secure data handling, with an integrated Human-in-the-Loop (HITL) mechanism via messaging platforms like Telegram for handling uncertainties.

## High-Level Overview

FormWhisperer adopts a **Monorepo** architectural style, enabling a unified development experience across distinct backend services (Node.js/TypeScript, Python) and a potential lightweight frontend. The core system operates by having a central orchestrator service that manages browser automation agents, persona data, and HITL interactions. Data flows from user-defined persona profiles, through the AI agent's processing of survey questions, to responses generated and submitted via the browser automation layer. When ambiguity arises, the HITL orchestrator routes the query to the user for real-time guidance.

Code snippet

[formwhisperer-c4](https://app.capacities.io/6002bb54-716f-4804-8c6a-17e1e219e363/ff7404d2-1320-4e9a-88a6-df570a4c630a)

```markdown
C4Container
    title FormWhisperer System Context
    Container(user, "User", "Human User", "Interacts for setup and HITL")
    Container(formWhisperer, "FormWhisperer System", "AI-Powered Form Automation Platform", "Automates online form completion with human-like intelligence")
    Container(externalSurveyPlatform, "External Survey Platform", "Web Application", "Hosts surveys to be completed")
    Rel(user, formWhisperer, "Configures, Provides HITL input to", "Web UI / Messaging App")
    Rel(formWhisperer, externalSurveyPlatform, "Completes forms on", "HTTP/Browser Automation")
```

Code snippet



```markdown
C4Component
    title FormWhisperer Container Diagram
    Container_Boundary(formWhispererSystem, "FormWhisperer System") {
        Component(webUI, "Web UI Service", "React/Next.js", "Provides Persona Setup & Management UI. Optional MVP.")
        Component(personaService, "Persona Service", "Node.js/Express (TypeScript), MongoDB", "Manages user personas; stores and retrieves profiles.")
        Component(hitlService, "HITL Orchestration Service", "Node.js/Express (TypeScript), Telegram API", "Manages human-in-the-loop interactions; sends/receives messages.")
        Component(automationOrchestrator, "Automation Orchestrator", "Node.js (TypeScript)", "Coordinates browser automation agents and AI response generation for surveys.")
        Component(browserAutomator, "Browser Automator", "Python, Browser Use / Browser MCP", "Controls browser instance, navigates, interacts with UI elements (clicks, types, scrolls).")
        Component(responseGenerator, "Response Generator", "Python, LLM, LangChain", "Analyzes survey questions, generates persona-consistent answers.")
        Component(formParser, "Form Parser", "Python", "Identifies and extracts details from various form field types on web pages.")
        Component(llm, "Large Language Model", "External API (e.g., Gemini, OpenAI)", "Provides core natural language understanding and generation capabilities.")
        Rel(webUI, personaService, "Configures personas via")
        Rel(hitlService, webUI, "Notifies via (optional in MVP)", "Websockets/API")
        Rel(automationOrchestrator, personaService, "Retrieves personas from")
        Rel(automationOrchestrator, browserAutomator, "Sends browser commands to")
        Rel(automationOrchestrator, responseGenerator, "Sends questions to")
        Rel(automationOrchestrator, formParser, "Receives form data from")
        Rel(browserAutomator, automationOrchestrator, "Sends form data to")
        Rel(browserAutomator, externalSurveyPlatform, "Interacts with", "HTTP/Browser Automation")
        Rel(responseGenerator, llm, "Queries for answers", "API")
        Rel(responseGenerator, personaService, "Retrieves persona context from")
        Rel(formParser, browserAutomator, "Extracts form structure from")
        Rel(hitlService, automationOrchestrator, "Sends HITL prompts from / Receives HITL responses for")
        Rel(automationOrchestrator, hitlService, "Requests HITL from")
        Container_Boundary(formWhispererSystem, "External Survey Platform") {
            Component(surveyHost, "Survey Hosting Platform", "Web Application", "Where forms reside")
            Rel(browserAutomator, surveyHost, "Automates completion on")
        }
    }
```

## Architectural / Design Patterns Adopted

- **Microservices (within Monorepo):** For clear separation of concerns, allowing specialized teams/agents (e.g., browser automation, persona management, HITL) to operate independently.

- **Facade Pattern:** The `Automation Orchestrator` acts as a facade, simplifying the interface to the underlying browser automation, form parsing, and response generation complexities.

- **Observer Pattern (for HITL):** The `HITL Orchestration Service` could use an observer pattern to notify the user (via messaging app) and await a response.

- **Strategy Pattern:** The `Response Generator` might employ different strategies for answering based on question type (e.g., open-ended, multiple choice, demographic) and persona depth.

- **Repository Pattern:** The `Persona Service` will likely abstract data access to the MongoDB.

## Component View

- **Web UI Service:** (React/Next.js) - Responsible for providing a user interface for initial persona setup, potentially monitoring agent status, and displaying HITL prompts (though HITL is primarily external messaging).

- **Persona Service:** (Node.js/Express/MongoDB) - Manages the creation, storage, retrieval, and updating of user persona profiles. It provides an API for other internal services to access persona data.

- **HITL Orchestration Service:** (Node.js/Express, Telegram Bot API) - Handles communication with external messaging platforms (e.g., Telegram) to send HITL requests to the user and receive their responses, relaying them back to the automation orchestrator.

- **Automation Orchestrator:** (Node.js) - The central brain. It receives tasks (e.g., "complete survey"), orchestrates the `Browser Automator`, `Form Parser`, and `Response Generator`, and triggers the `HITL Service` when human intervention is needed.

- **Browser Automator:** (Python, Browser Use/Browser MCP) - The direct interface to the web browser. It executes commands from the `Automation Orchestrator` to navigate, click, type, scroll, and retrieve page content. It's responsible for the "human-like" interaction patterns.

- **Form Parser:** (Python) - Analyzes the HTML DOM received from the `Browser Automator` to identify form fields, their types, and associated labels/questions. It provides a structured representation of the form to the `Response Generator`.

- **Response Generator:** (Python, LLM, LangChain) - Consumes questions from the `Form Parser` (via `Automation Orchestrator`), retrieves persona context from the `Persona Service`, and generates appropriate, persona-consistent answers using a Large Language Model (LLM).

- **Large Language Model (LLM):** (External API) - The underlying AI for natural language understanding and generation, providing the core intelligence for the `Response Generator`.

## Project Structure

Plaintext

```text
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

### Key Directory Descriptions

- `docs/`: Contains all project planning and reference documentation.

- `src/services/`: Houses backend services developed in Node.js/TypeScript, each as a distinct microservice-like module.

- `src/agents/`: Contains Python-based components for AI and browser automation, also structured as modular services.

- `src/shared/`: For common TypeScript types, interfaces, and utilities shared across Node.js services and the frontend.

- `src/agents/shared-python/`: For common Python modules and utilities shared across Python agents.

- `src/web-ui/`: Contains the frontend application source code.

- `test/`: Contains all automated tests, mirroring the `src/` structure where applicable.

### Notes

The monorepo approach uses npm/yarn workspaces to manage dependencies and scripts across services. Each service/agent will have its own `package.json` (or `pyproject.toml` for Python) for its specific dependencies.

## API Reference

### External APIs Consumed

#### Large Language Model (LLM) API (e.g., Gemini, OpenAI GPT)

- **Purpose:** Core for natural language understanding and generation in `Response Generator`.

- **Base URL(s):**

    - Production: `{LLM_API_PRODUCTION_URL}`

    - Staging/Dev: `{LLM_API_STAGING_URL}`

- **Authentication:** API Key in Header (`Authorization: Bearer {API_KEY}`)

- **Key Endpoints Used:**

    - `POST /v1/chat/completions` (or similar for text generation)

        - Description: Generates text responses based on prompt and persona.

        - Request Body Schema: `{ "model": "...", "messages": [{ "role": "user", "content": "..." }], "temperature": 0.7 }` (example for OpenAI Chat Completions API)

        - Success Response Schema: `{ "choices": [{ "message": { "content": "..." } }] }`

- **Rate Limits:** To be observed per LLM provider's documentation.

- **Link to Official Docs:** `{URL_TO_LLM_PROVIDER_DOCS}`

#### Telegram Bot API (for HITL)

- **Purpose:** Sending HITL prompts to the user and receiving responses.

- **Base URL(s):** `https://api.telegram.org/bot{BOT_TOKEN}/`

- **Authentication:** Bot Token in URL.

- **Key Endpoints Used:**

    - `POST /sendMessage`

        - Description: Sends a text message to a user or chat.

        - Request Body Schema: `{ "chat_id": "...", "text": "...", "reply_markup": {...} }`

    - `POST /getUpdates`

        - Description: Receives incoming updates (messages from users).

- **Rate Limits:** Adhere to Telegram's limits (e.g., 30 messages/second per bot to the same chat).

- **Link to Official Docs:** `https://core.telegram.org/bots/api`

### Internal APIs Provided

#### Persona Service API

- **Purpose:** Provides API for managing user personas.

- **Base URL(s):** `/api/v1/personas`

- **Authentication/Authorization:** Internal service-to-service authentication (e.g., API key, JWT for internal calls).

- **Endpoints:**

    - `POST /`

        - Description: Creates a new persona.

        - Request Body Schema: `{"name": "string", "demographics": {}, "preferences": {}, "opinions": {}}`

        - Success Response Schema: `{"id": "string", "name": "string", ...}`

    - `GET /{id}`

        - Description: Retrieves a persona by ID.

        - Success Response Schema: `{"id": "string", "name": "string", ...}`

    - `PUT /{id}`

        - Description: Updates an existing persona.

        - Request Body Schema: `{"name": "string", "demographics": {}, ...}`

    - `GET /current` (if user-specific persona via UI)

        - Description: Retrieves the currently active user's persona.

#### HITL Orchestration Service API

- **Purpose:** Internal API for the Automation Orchestrator to request HITL.

- **Base URL(s):** `/api/v1/hitl`

- **Authentication/Authorization:** Internal service-to-service authentication.

- **Endpoints:**

    - `POST /request`

        - Description: Sends a human-in-the-loop request.

        - Request Body Schema: `{"userId": "string", "question": "string", "context": "string", "options": ["string"], "callbackUrl": "string"}`

        - Success Response Schema: `{"hitlRequestId": "string"}`

## Data Models

### Core Application Entities / Domain Objects

#### Persona

- **Description:** Represents a simulated user profile for form completion.

- **Schema / Interface Definition:**

    TypeScript

    ```typescript
    export interface Persona {
      id: string; // Unique identifier for the persona
      userId: string; // ID of the human user this persona belongs to
      name: string; // Display name of the persona (e.g., "My Default Persona", "Tech Enthusiast")
      demographics: {
        ageRange?: string; // e.g., "25-34"
        gender?: string; // e.g., "Male", "Female", "Non-binary"
        incomeRange?: string; // e.g., "50k-75k"
        raceEthnicity?: string[]; // e.g., ["White", "Asian"]
        educationLevel?: string; // e.g., "Bachelors"
        country?: string;
        // ... more demographic details
      };
      preferences: {
        productCategories?: string[]; // e.g., ["Electronics", "Software"]
        shoppingHabits?: string; // e.g., "Online frequently"
        // ... more specific preferences
      };
      opinions: {
        [topic: string]: string; // Key-value pairs for specific opinions, e.g., "abortion": "legal", "AI_ethics": "regulated"
      };
      responseStyle: {
        verbosity?: "concise" | "moderate" | "verbose";
        tone?: "formal" | "neutral" | "casual";
        // ... other stylistic elements
      };
      createdAt: Date;
      updatedAt: Date;
    }
    ```

- **Validation Rules:** `userId` must be a valid UUID. `name` max length 100 characters. Demographic fields should conform to predefined enum values where applicable.

#### SurveyCompletionRecord

- **Description:** Stores metadata and details of a completed survey by an AI agent.

- **Schema / Interface Definition:**

    TypeScript

    ```typescript
    export interface SurveyCompletionRecord {
      id: string; // Unique ID for the completion record
      personaId: string; // ID of the persona used
      surveyUrl: string; // URL of the completed survey
      platformName: string; // Name of the survey platform
      completionStatus: "completed" | "partial" | "failed" | "hitl_paused";
      startTime: Date;
      endTime?: Date;
      durationSeconds?: number;
      responses: Array<{ // Optional: store key responses for analysis
        question: string;
        answer: string;
        questionType: "text" | "dropdown" | "radio" | "checkbox" | "open_ended";
        hitlInvolved: boolean; // Was HITL used for this answer?
      }>;
      hitlRequests: Array<{ // Log of HITL interactions for this survey
        requestId: string;
        timestamp: Date;
        question: string;
        context: string;
        humanResponse?: string;
      }>;
      notes: string; // Any notes or errors during completion
    }
    ```

### Database Schemas (MongoDB Collections)

#### `personas` Collection

- **Purpose:** Stores `Persona` documents.

- **Schema Definition:** Corresponds to the `Persona` interface above, with appropriate indexing on `userId` and `id`.

#### `surveyCompletionRecords` Collection

- **Purpose:** Stores `SurveyCompletionRecord` documents.

- **Schema Definition:** Corresponds to the `SurveyCompletionRecord` interface above, with indexing on `personaId`, `completionStatus`, and `startTime`.

## Core Workflow / Sequence Diagrams

### Survey Completion Workflow (Happy Path)

Code snippet

```markdown
sequenceDiagram
    actor User
    participant WebUI
    participant AOS as Automation Orchestrator Service
    participant PS as Persona Service
    participant BA as Browser Automator
    participant FP as Form Parser
    participant RG as Response Generator
    participant LLM as LLM API
    participant ESP as External Survey Platform
    User->>WebUI: Initiate Survey Completion (e.g., provide URL, select Persona)
    WebUI->>AOS: Request Start Survey (url, personaId)
    AOS->>PS: Get Persona Data (personaId)
    PS-->>AOS: Return Persona Data
    AOS->>BA: Launch Browser & Navigate (url)
    BA->>ESP: Load Survey Page
    ESP-->>BA: Rendered Survey Page
    loop For each form question
        BA->>FP: Get Current Page DOM
        FP-->>BA: Return Parsed Form Elements (question, type, options)
        BA->>AOS: Send Form Elements
        AOS->>RG: Request Answer (question, type, options, personaData)
        RG->>LLM: Query for Answer (question, personaData, context)
        LLM-->>RG: Return Raw Answer
        RG-->>AOS: Return Processed Answer
        AOS->>BA: Fill Form Field (answer)
        BA->>ESP: Interact with Form (type, click, select)
        ESP-->>BA: Next Question / Submit
    end
    BA->>AOS: Survey Completed
    AOS->>PS: Store SurveyCompletionRecord
    PS-->>AOS: Confirmation
    AOS->>WebUI: Notify Survey Complete
    WebUI->>User: Display Completion Status
```

### Human-in-the-Loop (HITL) Workflow

Code snippet

```markdown
sequenceDiagram
    actor User
    participant AOS as Automation Orchestrator Service
    participant HS as HITL Service
    participant MP as Messaging Platform (e.g., Telegram)
    participant RG as Response Generator
    participant BA as Browser Automator
    BA->>AOS: Detected Ambiguity / Low Confidence (question, context)
    AOS->>RG: Request Answer (question, context, personaData)
    RG->>RG: Evaluate Confidence
    alt Low Confidence
        RG->>AOS: Signal HITL Required (question, context, options)
        AOS->>HS: Send HITL Request (userId, question, context, options)
        HS->>MP: Send Message to User
        MP-->>User: Notification
        User->>MP: Provide Response
        MP-->>HS: Forward User Response
        HS-->>AOS: Return User Response
        AOS->>RG: Retry Answer with Human Input (question, context, options, humanInput)
        RG->>LLM: Re-query with Human Input (optional)
        LLM-->>RG: Return Refined Answer
        RG-->>AOS: Return Confident Answer
    else High Confidence
        RG-->>AOS: Return Confident Answer
    end
    AOS->>BA: Fill Form Field (answer)
    BA->>ESP: Interact with Form
```

## Definitive Tech Stack Selections

This table is the **single source of truth** for all technology selections. Other architecture documents (e.g., Frontend Architecture) must refer to these choices and elaborate on their specific application rather than re-defining them.

| Category             | Technology                        | Version / Details                        | Description / Purpose                                                                     | Justification (Optional)                                                                          |
| :------------------- | :-------------------------------- | :--------------------------------------- | :---------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------ |
| **Languages**        | TypeScript                        | 5.x                                      | Primary language for Node.js backend services and web frontend.                           | Strong typing, large ecosystem, good for complex service orchestration.                           |
|                      | Python                            | 3.11                                     | Used for AI/ML components (persona modeling, response generation) and browser automation. | Rich AI/ML libraries, strong scripting capabilities for automation.                               |
| **Runtime**          | Node.js                           | 22.x                                     | Server-side execution environment for orchestrator and other backend services.            | High performance for I/O bound tasks, large package ecosystem.                                    |
| **Frameworks**       | NestJS / Express.js               | Latest (e.g., NestJS 10.x / Express 4.x) | Backend API framework for persona, HITL, and automation orchestrator services.            | NestJS for structured, enterprise-grade applications; Express for simplicity in smaller services. |
|                      | FastAPI                           | Latest (e.g., 0.111.x)                   | Python web framework for AI/automation services, known for performance and type hints.    | High performance, automatic OpenAPI documentation, good for data-intensive APIs.                  |
|                      | React                             | Latest (e.g., 18.x)                      | Frontend UI library for persona setup/management.                                         | Component-based, large community, suitable for dynamic UIs.                                       |
|                      | Next.js                           | Latest (e.g., 14.x)                      | React framework for web UI (SSR, routing).                                                | Provides full-stack capabilities, server-side rendering for performance.                          |
| **Databases**        | MongoDB                           | 7.0                                      | Primary NoSQL data store for flexible persona data and survey completion records.         | Schema flexibility suits varied persona attributes and evolving survey data.                      |
| **Cloud Platform**   | AWS                               | N/A                                      | Primary cloud provider for hosting all services.                                          | Comprehensive suite of services, scalability, reliability.                                        |
| **Cloud Services**   | AWS Lambda                        | N/A                                      | Serverless compute for stateless backend functions (e.g., HITL trigger).                  | Cost-effective, scales automatically.                                                             |
|                      | AWS S3                            | N/A                                      | Object storage for static assets (e.g., frontend build artifacts).                        | Highly durable, scalable, cost-effective storage.                                                 |
|                      | AWS DynamoDB                      | N/A                                      | (Consider for high-performance, key-value data, e.g., session state for agents).          | High performance, fully managed NoSQL for specific high-throughput needs.                         |
| **Infrastructure**   | AWS CDK                           | Latest                                   | Infrastructure as Code (IaC) tool for defining and provisioning AWS resources.            | Uses familiar programming languages, good for complex cloud setups.                               |
|                      | Docker                            | Latest                                   | Containerization for deploying services consistently across environments.                 | Portability, isolation, consistent runtime.                                                       |
| **UI Libraries**     | Tailwind CSS                      | Latest (e.g., 3.x)                       | Utility-first CSS framework for rapid UI styling.                                         | Highly customizable, efficient for reactive design.                                               |
| **State Management** | Zustand                           | Latest (e.g., 4.x)                       | Frontend state management for the web UI.                                                 | Simple, fast, and scalable for React applications.                                                |
| **Testing**          | Jest                              | Latest (e.g., 29.x)                      | Unit/Integration testing framework for Node.js (TypeScript) and React.                    | Widely adopted, good for mocking, snapshot testing.                                               |
|                      | Playwright                        | Latest (e.g., 1.44.x)                    | End-to-end testing framework for browser automation.                                      | Supports multiple browsers, strong for E2E tests, can run alongside Browser Use/MCP.              |
|                      | Pytest                            | Latest (e.g., 8.x)                       | Unit/Integration testing framework for Python agents.                                     | Simple, extensible, widely used in Python community.                                              |
| **CI/CD**            | GitHub Actions                    | N/A                                      | Continuous Integration/Deployment pipeline automation.                                    | Integrated with GitHub, flexible workflows.                                                       |
| **Other Tools**      | LangChain.js / LangChain (Python) | Latest                                   | Library for integrating LLMs and orchestrating complex AI workflows.                      | Facilitates interaction with LLMs, prompt engineering.                                            |
|                      | Browser Use                       | Latest                                   | Primary framework for robust browser automation and interaction.                          | Specified by user for performance and reliability.                                                |
|                      | Browser MCP                       | Latest                                   | Alternative/complementary framework for high-performance browser automation.              | Specified by user for advanced automation needs.                                                  |

Export to Sheets

## Infrastructure and Deployment Overview

- **Cloud Provider(s):** AWS

- **Core Services Used:** AWS Lambda (for stateless services), AWS S3 (static assets), AWS EC2 (for services requiring dedicated instances, e.g., browser automation might run on EC2 or Fargate), AWS RDS (if relational DB considered later), AWS DynamoDB (for specific NoSQL needs), AWS ECS/Fargate (for containerized services).

- **Infrastructure as Code (IaC):** AWS CDK - Location: `infra/` directory within the monorepo.

- **Deployment Strategy:** CI/CD pipeline with automated promotions (e.g., `dev` -> `staging` -> `production`). Blue/Green deployment or Canary releases for critical updates will be considered where appropriate to minimize downtime.

- **Tools:** GitHub Actions for CI/CD automation. Docker for containerization of all services.

- **Environments:** Development (local), Staging (AWS), Production (AWS).

- **Environment Promotion:** Automated after tests pass for `dev` to `staging`. Manual approval after `staging` tests pass, then automated to `production` after passing production readiness checks.

- **Rollback Strategy:** Automated rollback to previous stable version on health check failure post-deployment, or manual trigger via CI/CD job. Docker containerization and IaC state management support efficient rollbacks.

## Error Handling Strategy

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

## Coding Standards

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

- **File Structure:** Adhere to the layout defined in the "Project Structure" section.

- **Unit Test File Organization:**

    - **TypeScript/Node.js:** `*.test.ts` or `*.spec.ts` co-located with source files (e.g., `src/services/persona-service/src/index.test.ts`).

    - **Python:** `test_*.py` files located in a parallel `test/unit/` directory, mirroring the `src/agents/` structure (e.g., `test/unit/agents/browser-automator/test_main.py`).

- **Asynchronous Operations:** Always use `async`/`await` for promise-based operations (TypeScript/Python).

- **Type Safety:**

    - **TypeScript:** Strict mode (all flags enabled) in `tsconfig.json`. Avoid `!` non-null assertion operator; prefer explicit checks, optional chaining (`?.`), or nullish coalescing (`??`).

    - **Python:** All new functions and methods must have full type hints. MyPy will be enforced in CI.

    - **Type Definitions:** Global types in `src/shared/types/`. Policy on using `any` or equivalent is strongly discouraged and requires justification.

- **Comments & Documentation:**

    - Code Comments: Explain *why*, not *what*, for complex logic. Use JSDoc (TypeScript), Python docstrings (Google style).

    - READMEs: Each `src/services/` and `src/agents/` module will have a README.md.

- **Dependency Management:** `npm`/`yarn` workspaces for Node.js, Poetry/Pipenv for Python. Prefer pinned versions for stability. New dependencies require security scans and approval.

### Detailed Language & Framework Conventions

#### TypeScript/Node.js (for `src/services/`, `src/web-ui/`)

- **Immutability:** Always prefer immutable data structures. Use `Readonly<T>`, `ReadonlyArray<T>`, `as const`. Avoid direct mutation of objects/arrays passed as props or state.

- **Functional vs. OOP:** Favor functional programming constructs (map, filter, reduce, pure functions) for data transformation. Use classes for services, controllers, or when NestJS conventions dictate.

- **Error Handling Specifics:** Always use `Error` objects for `throw`. Custom error classes inherit from `AppError` for domain-specific errors.

- **Null/Undefined Handling:** `strictNullChecks` enabled. Avoid `!`. Use `?.` or `??`.

- **Module System:** ESModules (`import`/`export`) exclusively.

- **Logging Specifics:** Use `Pino` for structured JSON logs. Include `correlationId`. Do not log sensitive PII.

- **Framework Idioms (NestJS/Express):** NestJS: Use decorators for modules, controllers, services, DTOs. Adhere to dependency injection. Express: Middleware patterns, routing structure.

- **Key Library Usage:** Axios for HTTP with configured instance. `date-fns` for date/time.

#### Python (for `src/agents/`)

- **Immutability:** Use tuples for immutable sequences. `@dataclass(frozen=True)` where appropriate.

- **Functional vs. OOP:** Classes for entities and services. Functions for stateless operations. List comprehensions preferred.

- **Error Handling Specifics:** Raise specific, custom exceptions inheriting from `AppException`. Use `try-except-else-finally`. Avoid broad `except Exception:`.

- **Resource Management:** Always use `with` statements (e.g., for files, DB connections).

- **Type Hinting:** All new functions/methods must have full type hints. MyPy enforced in CI.

- **Logging Specifics:** Use Python's `logging` module with `structlog` for structured JSON output. Include `correlationId`.

- **Framework Idioms (FastAPI):** Utilize Pydantic for request/response models. Dependency injection for services.

- **Key Library Usage:** `httpx` or `requests` for HTTP with explicit timeouts.

## Overall Testing Strategy

This section outlines the project's comprehensive testing strategy, which all AI-generated and human-written code must adhere to.

- **Tools:** Jest, Playwright, Pytest.

- **Unit Tests:**

    - **Scope:** Test individual functions, methods, classes, or small modules in isolation. Focus on business logic, algorithms, and data transformations.

    - **Location:**

        - **TypeScript/Node.js:** `*.test.ts` or `*.spec.ts` co-located with source files.

        - **Python:** `test_*.py` in a parallel `test/unit/` directory mirroring the `src/` structure.

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

## Security Best Practices

- **Input Sanitization/Validation:** All external inputs (API requests, user-provided data, form fields from surveys) must be sanitized and validated using `class-validator` with DTOs (TypeScript) or Pydantic (Python). Validation must occur at the service boundary.

- **Output Encoding:** React's JSX auto-escaping will be relied upon for frontend. For backend-generated content, use contextually appropriate encoding libraries (e.g., `html-entities` for HTML, JSON stringify for JSON) to prevent XSS.

- **Secrets Management:** Environment variables (`.env`, AWS Secrets Manager) for all secrets (API keys, database credentials, bot tokens). Never hardcode secrets or commit them to source control. Access via a designated configuration module/service.

- **Dependency Security:** Automated vulnerability scans (`npm audit`, `pip-audit`, Snyk, Dependabot) in CI. High/critical vulnerabilities addressed promptly.

- **Authentication/Authorization Checks:** All internal service APIs (except explicitly public ones) must enforce authentication/authorization using internal API keys or short-lived JWTs. The `Persona Service` and `HITL Orchestration Service` will have strict access controls.

- **Principle of Least Privilege (Implementation):** Database users will have minimal necessary permissions. AWS IAM roles will be narrowly scoped to specific actions and resources for each service.

- **API Security (General):** Enforce HTTPS for all communication. Implement rate limiting and throttling on exposed APIs. Use standard HTTP security headers (CSP, HSTS).

- **Error Handling & Information Disclosure:** Error messages must not leak sensitive information (stack traces, internal paths) to clients. Log detailed errors server-side, provide generic messages or error IDs to the client.

- **Regular Security Audits/Testing:** SAST/DAST tools integrated into CI.

## Key Reference Documents

(This section will be populated during the document sharding task)

## Change Log

| Change        | Date       | Version | Description                                           | Author            |
| :------------ | :--------- | :------ | :---------------------------------------------------- | :---------------- |
| Initial Draft | 2025-07-10 | 1.0     | Comprehensive Architecture Document for FormWhisperer | Ava "Atlas" Patel |
