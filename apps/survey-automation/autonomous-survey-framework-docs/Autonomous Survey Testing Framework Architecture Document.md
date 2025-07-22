---
type: Page
title: Autonomous Survey Testing Framework Architecture Document
description: null
icon: null
createdAt: '2025-06-18T03:15:39.576Z'
creationDate: 2025-06-17 22:15
modificationDate: 2025-06-18 00:12
tags: []
coverImage: null
---

# Autonomous Survey Testing Framework Architecture Document

# **Autonomous Survey Testing Framework Architecture Document**

## **1. Introduction / Preamble**

This document outlines the overall project architecture for the Autonomous Survey Testing Framework. It covers the backend systems, frontend user interface, inter-component communication, and all non-UI specific concerns. Its primary goal is to serve as the guiding architectural blueprint for development, ensuring consistency and adherence to the chosen patterns and technologies, with a primary constraint of being zero-cost and open-source for the MVP.

## **2. Technical Summary**

The architecture consists of two primary components within a Turborepo monorepo: a Python-based backend agent and a Next.js frontend dashboard. The backend agent, built on the Skyvern framework, handles the core automation logic, scheduling, and browser interaction. The Next.js application serves as a Backend-for-Frontend (BFF), providing a user interface for data management and a real-time dashboard for monitoring the agent. Communication between the frontend and backend is achieved via WebSockets for real-time data streaming and a simple REST API for control commands. The entire system is containerized with Docker for consistent local deployment.

## **3. High-Level Overview**

The architectural style is a monolith within a monorepo, but with a clear logical separation of concerns between the frontend and backend applications. The Next.js application acts as the primary user entry point, orchestrating control and observation of the Python agent.

Code snippet

```text
graph TD
    subgraph "User's Local Machine"
    User -- "Interacts via Browser" --> A["Next.js Dashboard & BFF"];
    A -- "REST (Pause/Resume) & WebSocket (Logs/Status)" <--> B["Python Backend Agent (Skyvern)"];
    B -- "Controls" --> C["Headless Browser (Dockerized)"];
    C -- "Takes Surveys" --> D[("External Survey Websites")];
    end
```

## **4. Architectural / Design Patterns Adopted**

- **Monorepo:** Utilizes Turborepo to manage the Python backend and Next.js frontend within a single repository, simplifying dependency management and cross-application scripting.

- **Containerization:** The entire application stack (backend, frontend) will be containerized using Docker and managed via `docker-compose`. This ensures a consistent and reproducible environment.

- **Scheduler-Worker Pattern:** The backend agent employs a scheduler (APScheduler) to trigger survey-taking jobs (workers) at regular intervals, enabling continuous, autonomous operation.

- **Backend for Frontend (BFF):** The Next.js application serves not only the UI but also contains API routes. These routes act as a proxy and control layer to the Python backend, simplifying frontend logic and managing communication.

## **5. Component View**

- **Frontend Dashboard (Next.js):** A React-based application responsible for all user interactions.

    - **Data Management:** Provides UI for creating/editing user profiles and uploading configuration files.

    - **Live Dashboard:** Displays real-time logs and a live view of the browser controlled by the agent.

    - **Control Interface:** Sends commands (pause, resume) to the backend via its API routes.

- **Backend Agent (Python/Skyvern):** The core automation engine.

    - **Task Scheduler:** Manages the timing and execution of survey jobs.

    - **Workflow Executor:** Uses Skyvern to interact with browser-based survey applications.

    - **State & Communication API:** Exposes a simple API (e.g., FastAPI) and a WebSocket server to allow control and observation from the frontend.

- **Communication Layer (WebSocket & REST):**

    - **WebSockets:** Used for streaming real-time data (logs, status updates) from the backend agent to the frontend dashboard for low-latency updates.

    - **REST API:** A simple set of endpoints for state-changing commands like `pause` and `resume`.

## **6. Project Structure**

Plaintext

```text
survey-automation-framework/
├── apps/
│   ├── backend-agent/        # Python/Skyvern application
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py       # Entry point with Scheduler & API
│   │   │   └── agent.py      # Core agent logic
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── frontend-dashboard/   # Next.js application
│       ├── app/              # Next.js App Router
│       ├── components/
│       ├── Dockerfile
│       └── package.json
├── packages/
│   ├── ui/                   # Shared React components (optional)
│   └── tsconfig/             # Shared TypeScript configs
├── docker-compose.yml        # To orchestrate local services
├── .gitignore
├── package.json              # Root package.json
└── turbo.json
```

## **7. API Reference (Internal)**

### REST API (Exposed by Backend Agent)

- `POST /agent/pause`: Signals the agent to pause its current workflow.

- `POST /agent/resume`: Signals a paused agent to resume its workflow.

### WebSocket Communication

- **Connection:** The frontend establishes a WebSocket connection to the backend agent.

- **Messages from Backend to Frontend:**

    - `{ "type": "log", "payload": "Log message here..." }`

    - `{ "type": "status", "payload": "Running" | "Paused" | "Resting" }`

- **VNC for Browser View:** A lightweight VNC server will be run alongside the browser instance, and the frontend will use a JavaScript VNC client (e.g., noVNC) to render the live view.

## **8. Data Models**

### User Profile (`config.yml.enc`)

YAML

```text
user_profile:
  name: "John Doe"
  email: "johndoe@example.com"
  # ... other demographic data
custom_answers:
  - question: "Question text"
    answer: "Answer text"
```

## **9. Definitive Tech Stack Selections**

| Category         | Technology              | Version / Details | Purpose                          |
| :--------------- | :---------------------- | :---------------- | :------------------------------- |
| **Languages**    | Python                  | 3.10+             | Backend Agent Logic              |
|                  | TypeScript              | 5.x               | Frontend Application             |
| **Frameworks**   | Skyvern                 | Latest            | Core Browser Automation          |
|                  | Next.js                 | 14.x              | Frontend UI & BFF                |
|                  | FastAPI                 | Latest            | Backend API/WebSocket Server     |
| **Scheduling**   | APScheduler             | Latest            | Continuous Job Scheduling        |
| **Tooling**      | Turborepo               | Latest            | Monorepo Management              |
|                  | Docker & Docker Compose | Latest            | Containerization & Orchestration |
| **UI Libraries** | Tailwind CSS            | Latest            | Styling                          |
|                  | shadcn/ui               | Latest            | Headless UI Components           |
| **Testing**      | Pytest                  | Latest            | Backend Unit Tests               |
|                  | Jest & RTL              | Latest            | Frontend Unit/Component Tests    |
| **CI/CD**        | GitHub Actions          | N/A               | Automated Build & Test           |

Export to Sheets

## **10. Infrastructure and Deployment Overview**

- **Cloud Provider:** None. The system is designed to run locally on a user's machine to adhere to the zero-cost constraint.

- **Infrastructure as Code (IaC):** Not applicable for the MVP.

- **Deployment Strategy:** Development and execution will be managed via `docker-compose`. The CI/CD pipeline in GitHub Actions will build and test the Docker images on every push to `main`, but deployment is a manual `docker-compose up` action on the local machine.

## **11. Coding Standards**

- **Python:** Code will be formatted using `Black` and linted with `Flake8`.

- **TypeScript/JS:** Code will be formatted using `Prettier` and linted with `ESLint`.

- **File Naming:** `kebab-case` for frontend components, `snake_case` for Python files.

- **Environment Variables:** All secrets (e.g., decryption key) and configurations (e.g., scheduler interval) will be managed through environment variables and a `.env` file, which will not be committed to source control.

## **12. Overall Testing Strategy**

- **Unit Tests:** Backend logic will be tested with `pytest`. Frontend components will be tested with `Jest` and `React Testing Library`. The CI pipeline will run these tests automatically.

- **Integration & E2E Tests:** As per the PRD, these will be conducted manually by the user for the MVP.

---

