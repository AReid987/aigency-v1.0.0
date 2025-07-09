---
type: Page
title: Sportsclub Architecture -> FINAL
description: null
icon: null
createdAt: '2025-06-05T22:14:04.112Z'
creationDate: 2025-06-05 17:14
modificationDate: 2025-06-05 17:17
tags: []
coverImage: null
---

# Sportsclub Architecture -> FINAL

Here is the complete, finalized Sportsclub Architecture Document, incorporating all our discussions and architectural decisions:

---

# Sportsclub Architecture Document

## Introduction / Preamble

This document outlines the overall project architecture for Sportsclub, including backend systems, shared services, and non-UI specific concerns. Its primary goal is to serve as the guiding architectural blueprint for AI-driven development, ensuring consistency and adherence to chosen patterns and technologies.

Relationship to Frontend Architecture:

Sportsclub includes a significant user interface, and a separate Frontend Architecture Document (linked in the "Key Reference Documents" section) will detail the frontend-specific design. This document (architecture.md) must be used in conjunction with the Frontend Architecture Document. Core technology stack choices documented herein (see "Definitive Tech Stack Selections" below) are definitive for the entire project, including any frontend components.

- **Link to Frontend Architecture Document (REQUIRED if exists):** (To be updated once the Frontend Architecture Document is created by the Design Architect)

## Table of Contents

- [Introduction / Preamble](https://www.google.com/search?q=%23introduction--preamble)

- [Technical Summary](https://www.google.com/search?q=%23technical-summary)

- [Architectural / Design Patterns Adopted](https://www.google.com/search?q=%23architectural--design-patterns-adopted)

- [Component View](https://www.google.com/search?q=%23component-view)

- [Project Structure](https://www.google.com/search?q=%23project-structure)

- [API Reference](https://www.google.com/search?q=%23api-reference)

- [Data Models](https://www.google.com/search?q=%23data-models)

- [Core Workflow / Sequence Diagrams](https://www.google.com/search?q=%23core-workflow--sequence-diagrams)

- [Definitive Tech Stack Selections](https://www.google.com/search?q=%23definitive-tech-stack-selections)

- [Infrastructure and Deployment Overview](https://www.google.com/search?q=%23infrastructure-and-deployment-overview)

- [Error Handling Strategy](https://www.google.com/search?q=%23error-handling-strategy)

- [Coding Standards](https://www.google.com/search?q=%23coding-standards)

- [Overall Testing Strategy](https://www.google.com/search?q=%23overall-testing-strategy)

- [Security Best Practices](https://www.google.com/search?q=%23security-best-practices)

- [Key Reference Documents](https://www.google.com/search?q=%23key-reference-documents)

- [Change Log](https://www.google.com/search?q=%23change-log)

## Technical Summary

Sportsclub will be a feature-rich web application leveraging a **Microservices architecture** within a **Monorepo managed by Turborepo**. The frontend will utilize **Next.js**, primarily deployed on **Vercel**, while backend microservices will reside on **AWS or GCP**, complemented by **Cloudflare** for edge services. **FastAPI** (Python) will serve as the primary backend framework, with **PostgreSQL** for relational data and **Redis** for caching and real-time needs. Data ingestion for odds and scores will combine **The Odds API** with **agent-powered scraping**, with a multi-agent validation and fallback strategy to ensure data quality. **WebSockets** will enable real-time communication for leaderboards and live chat. The system is designed for high scalability, reliability (targeting 99.5% uptime), and adherence to strict security and compliance standards.

## Architectural / Design Patterns Adopted

This section lists the key high-level patterns chosen for the architecture. These foundational patterns should be established early as they guide component design, interactions, and technology choices.

- **Microservices:** The application's backend will be composed of loosely coupled, independently deployable services, each responsible for a specific business capability. This supports scalability, resilience, and independent team development.

- **Monorepo:** All project codebases (frontend, backend services, shared libraries) will reside in a single repository managed by Turborepo. This facilitates code sharing, simplified dependency management, and atomic commits across services.

- **API Gateway Pattern:** All external requests to backend microservices will be routed through an API Gateway. This provides a single entry point, handles request routing, authentication, rate limiting, and potentially response transformation.

- **Event-Driven Architecture (for certain flows):** For asynchronous communication between microservices and to support real-time features like leaderboard updates and data ingestion pipelines, an event-driven approach (e.g., using message queues/brokers) will be utilized where appropriate.

- **Command Query Responsibility Segregation (CQRS) (for complex read/write operations):** For certain domains with high read-write disparity or complex querying needs (e.g., leaderboard data), CQRS may be explored to optimize performance and scalability by separating read and write models.

- **Repository Pattern:** A common pattern for abstracting data access logic, ensuring clean separation between business logic and data storage concerns.

- **Service Mesh (Future consideration for complex deployments):** For advanced microservices management, observability, and traffic control, a service mesh may be considered in future iterations.

## Component View

This section describes the major logical components or services of the system and their responsibilities, reflecting the decided overall architecture and the architectural patterns adopted.

![sportsclub-architecture-c4-system-context-flowchart-mmd](../MediaFiles/Images/sportsclub-architecture-c4-system-context-flowchart-mmd.svg)

[[sportsclub-architecture-c4-system-context-flowchart-mmd]]


```text
graph TD
    User(User) --- FE(Frontend Web App);
    subgraph Sportsclub Platform
        subgraph Edge Layer
            CDN(Cloudflare CDN) --- FE;
            FE --- API_GW(API Gateway);
        end
        subgraph Core Microservices
            API_GW --> AUS[Auth & User Service];
            API_GW --> SBS[Subscription & Billing Service];
            API_GW --> PES[Prediction Engine Service];
            API_GW --> DIS[Data Ingestion & Validation Service];
            API_GW --> LPS[Leaderboard & Prize Service];
            API_GW --> AIS[AI Assistant Service];
            API_GW --> CS[Content Service];
            API_GW --> ComS[Community Service];
            API_GW --> GS[Gamification Service];
            API_GW --> NS[Notification Service];
            DIS --> External_API(External Odds API / Scraped Data Sources);
            DIS --> DB_Raw[Raw Data Store];
            AUS --- DB_Auth(DB: Auth/User);
            SBS --- DB_Sub(DB: Subscriptions);
            PES --- DB_Pred(DB: Predictions);
            LPS --- DB_Leader(DB: Leaderboard);
            AIS --- DB_AI(DB: AI Knowledge Graph);
            CS --- DB_Content(DB: Content);
            ComS --- DB_Community(DB: Community);
            GS --- DB_Game(DB: Gamification);
            
            DB_Auth -- PostgreSQL --> DB_Persistent_P(Persistent Storage: PostgreSQL);
            DB_Sub -- PostgreSQL --> DB_Persistent_P;
            DB_Pred -- PostgreSQL --> DB_Persistent_P;
            DB_Leader -- Redis/PostgreSQL --> DB_Persistent_P;
            DB_AI -- Vector/Graph DB --> DB_Persistent_P;
            DB_Content -- PostgreSQL --> DB_Persistent_P;
            DB_Community -- PostgreSQL --> DB_Persistent_P;
            DB_Game -- PostgreSQL --> DB_Persistent_P;
            click FE "https://www.google.com/search?q=Next.js+Frontend+Application"
            click API_GW "https://www.google.com/search?q=API+Gateway+Pattern"
            click AUS "https://www.google.com/search?q=Authentication+and+User+Service"
            click SBS "https://www.google.com/search?q=Subscription+and+Billing+Service"
            click PES "https://www.google.com/search?q=Prediction+Engine+Service"
            click DIS "https://www.google.com/search?q=Data+Ingestion+and+Validation+Service"
            click LPS "https://www.google.com/search?q=Leaderboard+and+Prize+Service"
            click AIS "https://www.google.com/search?q=AI+Assistant+Service"
            click CS "https://www.google.com/search?q=Content+Service"
            click ComS "https://www.google.com/search?q=Community+Service"
            click GS "https://www.google.com/search?q=Gamification+Service"
            click NS "https://www.google.com/search?q=Notification+Service"
            click External_API "https://www.google.com/search?q=External+APIs+and+Scraping"
            click DB_Persistent_P "https://www.google.com/search?q=PostgreSQL+Database"
            click DB_Raw "https://www.google.com/search?q=Raw+Data+Storage"
            click DB_Auth "https://www.google.com/search?q=Database+per+Microservice+Authentication"
            click DB_Sub "https://www.google.com/search?q=Database+per+Microservice+Subscription"
            click DB_Pred "https://www.google.com/search?q=Database+per+Microservice+Prediction"
            click DB_Leader "https://www.google.com/search?q=Database+per+Microservice+Leaderboard"
            click DB_AI "https://www.google.com/search?q=Database+per+Microservice+AI"
            click DB_Content "https://www.google.com/search?q=Database+per+Microservice+Content"
            click DB_Community "https://www.google.com/search?q=Database+per+Microservice+Community"
            click DB_Game "https://www.google.com/search?q=Database+per+Microservice+Gamification"
            click CDN "https://www.google.com/search?q=Cloudflare+CDN"
            style FE fill:#bbf,stroke:#333,stroke-width:2px
            style API_GW fill:#f9f,stroke:#333,stroke-width:2px
            style AUS fill:#afa,stroke:#333,stroke-width:2px
            style SBS fill:#afa,stroke:#333,stroke-width:2px
            style PES fill:#afa,stroke:#333,stroke-width:2px
            style DIS fill:#afa,stroke:#333,stroke-width:2px
            style LPS fill:#afa,stroke:#333,stroke-width:2px
            style AIS fill:#afa,stroke:#333,stroke-width:2px
            style CS fill:#afa,stroke:#333,stroke-width:2px
            style ComS fill:#afa,stroke:#333,stroke-width:2px
            style GS fill:#afa,stroke:#333,stroke-width:2px
            style NS fill:#afa,stroke:#333,stroke-width:2px
            style External_API fill:#ffc,stroke:#333,stroke-width:2px
            style DB_Persistent_P fill:#ccf,stroke:#333,stroke-width:2px
            style DB_Raw fill:#ccf,stroke:#333,stroke-width:2px
            style DB_Auth fill:#eef,stroke:#333,stroke-width:1px
            style DB_Sub fill:#eef,stroke:#333,stroke-width:1px
            style DB_Pred fill:#eef,stroke:#333,stroke-width:1px
            style DB_Leader fill:#eef,stroke:#333,stroke-width:1px
            style DB_AI fill:#eef,stroke:#333,stroke-width:1px
            style DB_Content fill:#eef,stroke:#333,stroke-width:1px
            style DB_Community fill:#eef,stroke:#333,stroke-width:1px
            style DB_Game fill:#eef,stroke:#333,stroke-width:1px
            style CDN fill:#cff,stroke:#333,stroke-width:2px
            style User fill:#ccc,stroke:#333,stroke-width:2px
        end
    end
```

This diagram illustrates the high-level logical components and services, their relationships, and data flow within the Sportsclub platform, aligning with our microservices architecture. It also conceptually represents the "database per service" principle, with different microservices potentially using their own logical data stores, which then leverage a common persistent storage (like PostgreSQL) or specialized ones (like Redis for leaderboard).

- **Client Applications (Frontend & Mobile):**

    - **Frontend Web App:** The primary user interface for Sportsclub, built with Next.js and deployed on Vercel, consuming internal APIs.

    - (Future Mobile Apps - if applicable post-MVP).

- **API Gateway:** The entry point for all client-facing API requests, routing them to the appropriate microservices.

- **Authentication & User Service:**

    - Manages user registration, login (password/OAuth), ID verification, and user profiles.

    - Handles authentication tokens (e.g., JWTs) and authorization checks.

- **Subscription & Billing Service:**

    - Manages user subscriptions, recurring payments, and integrates with payment gateways (Stripe, Lemon Squeezy, etc.).

    - Handles subscription status and failures.

- **Prediction Engine Service:**

    - Manages the lifecycle of sporting events and predictions.

    - Handles prediction placement, validation of coin amounts, and recording of user picks.

- **Data Ingestion & Validation Service:**

    - Responsible for sourcing sports odds and real-time scores from external APIs (The Odds API) and dynamic scraping agents.

    - Implements the parallel agent swarm for cross-validation and fallback mechanisms (CRAG).

    - Provides clean, validated data to other services.

- **Leaderboard & Prize Service:**

    - Manages the real-time leaderboard data.

    - Manages the monthly prize calculation, awarding, and wallet reset process.

    - Handles prize claim and fulfillment (integrating with TBD legal/payment processes).

- **AI Assistant Service:**

    - Provides the backend logic for the AI assistant's capabilities: Q&A, generative UI for data visualization, tutoring, and personalized performance reviews.

    - Integrates with LLMs, prompt/response caching (Portkey), and knowledge graphs (Graphiti).

- **Content Service:**

    - Manages the sourcing, storage, and delivery of sports news articles (ticker, feed) and educational content.

- **Community Service:**

    - Manages forum functionality (posts, comments, voting, bookmarking).

    - Manages real-time chat functionality during live events.

    - Integrates with AI agents for moderation and facilitation.

- **Gamification Service:**

    - Tracks and awards daily bonus coins, login streaks, prediction win streaks.

    - Manages community challenges and activities.

- **Notification Service:**

    - Handles sending various notifications (in-app, email, SMS) for events like coin deposits, prediction results, and prize wins.

## Project Structure

This section provides an ASCII diagram representing the project's folder structure, reflecting the monorepo approach managed by Turborepo. The detailed structure for the frontend portion will be elaborated in the separate Frontend Architecture Document.

Plaintext

```text
{project-root}/
├── .github/                    # CI/CD workflows (e.g., GitHub Actions)
│   └── workflows/
│       └── main.yml
├── .vscode/                    # VSCode settings (optional)
├── build/                      # Compiled output (if applicable, often git-ignored)
├── config/                     # Static configuration files (if any)
├── docs/                       # Project documentation (PRD, Arch, UI/UX Spec, etc.)
│   ├── index.md
│   ├── prd.md
│   ├── ui-ux-spec.md
│   └── ... (other .md files)
├── infra/                      # Infrastructure as Code (e.g., CDK, Terraform)
│   └── lib/
│   └── bin/
├── node_modules/ / venv / target/ # Project dependencies (git-ignored)
├── packages/                   # Turborepo workspaces for microservices and frontend
│   ├── web/                    # Next.js Frontend Application
│   │   ├── src/
│   │   └── package.json
│   ├── auth-service/           # FastAPI Authentication & User Microservice
│   │   ├── src/
│   │   └── pyproject.toml
│   ├── prediction-service/     # FastAPI Prediction Engine Microservice
│   │   ├── src/
│   │   └── pyproject.toml
│   ├── data-ingestion-service/ # FastAPI Data Ingestion & Validation Microservice
│   │   ├── src/
│   │   └── pyproject.toml
│   ├── ai-assistant-service/   # FastAPI AI Assistant Microservice
│   │   ├── src/
│   │   └── pyproject.toml
│   ├── shared-libs/            # Shared code, types, utilities across services
│   │   ├── src/
│   │   └── package.json / pyproject.toml
│   └── ... (other microservices as defined in Component View)
├── scripts/                    # Utility scripts (build, deploy helpers, etc.)
├── test/                       # Automated tests (unit, integration, e2e, may be within packages too)
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore rules
├── package.json / pyproject.toml # Root project manifest and dependencies (Turborepo config)
├── tsconfig.json / pyproject.toml # Language-specific configuration (if applicable)
├── Dockerfile                  # Base Dockerfile for services
└── README.md                   # Project overview and setup instructions
```

### Key Directory Descriptions

- `docs/`: Contains all project planning and reference documentation (PRD, Architecture, UI/UX Spec, etc.).

- `infra/`: Holds the Infrastructure as Code definitions (e.g., AWS CDK, Terraform).

- `packages/`: The core of the monorepo, containing individual microservices (e.g., `auth-service`, `prediction-service`), the frontend application (`web`), and shared libraries (`shared-libs`).

- `scripts/`: Utility scripts for common tasks like building, testing, or deployment.

- `test/`: Contains automated tests, which may also be co-located within individual `packages/`.

## API Reference

This section outlines the APIs consumed by Sportsclub from external services and any internal APIs provided by Sportsclub's own microservices.

### External APIs Consumed

#### The Odds API

- **Purpose:** To source real-time sports odds for various major sporting events.

- **Base URL(s):** (To be specified by Architect during implementation)

- **Authentication:** (To be specified based on API provider requirements)

- **Key Endpoints Used:** (To be detailed by Architect based on API documentation)

    - `GET /sports`**:** Get a list of sports and their active markets.

    - `GET /odds`**:** Get the latest odds for a specific sport/event.

- **Rate Limits:** (To be identified and managed)

- **Link to Official Docs:** (URL to The Odds API documentation)

#### External Data Scraping Sources (Agent-Powered)

- **Purpose:** To dynamically acquire sports odds, real-time scores, and news content from various web sources, especially where dedicated APIs are unavailable or insufficient.

- **Key Tools:** Searxng, Tavily, Exa, Brave, Serp, AgentQL, Crawl4AI, Jina AI.

- **Authentication/Access:** Publicly accessible web content.

- **Data Structure:** Dynamic; requires robust parsing and validation.

- **Error Handling:** Implementation of Corrective RAG (CRAG) and fallback mechanisms for data quality issues.

### Internal APIs Provided (If Applicable)

- Each microservice (e.g., Authentication & User Service, Prediction Engine Service, Leaderboard & Prize Service, AI Assistant Service, Content Service, Community Service, Gamification Service) will expose its own internal API.

- **Purpose:** To enable secure and efficient communication between frontend applications and other microservices.

- **Base URL(s):** (Internal routing via API Gateway).

- **Authentication/Authorization:** Centralized authentication via API Gateway, with granular authorization controlled within each service.

- **Endpoints:** (Detailed endpoints, request/response schemas, and data models for each microservice API will be defined in the relevant service's documentation. JSON will be the standard data exchange format).

## Data Models

This section defines the main data models and entities the application works with, including their schemas and relationships. This will be a critical input for database design and API definitions.

### Core Application Entities / Domain Objects

- **User:** Represents a Sportsclub user.

    - **Schema / Interface Definition (Conceptual):**

        ```text
        interface User {
          id: string; // Unique identifier for the user.
          email: string; // User's registered email.
          username: string; // User's display name, changeable monthly.
          avatarUrl?: string; // URL to user's avatar image.
          age: number; // User's age (for legal age verification).
          address: string; // User's physical address (for legal/KYC).
          isVerified: boolean; // Status of ID verification.
          isSubscriber: boolean; // Current subscription status.
          roles: string[]; // User roles/permissions (e.g., 'user', 'moderator').
          // ... other profile-related properties
        }
        ```

        [https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png](https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png)Copy And Save[https://storage.googleapis.com/pieces-web-extensions-cdn/link.png](https://storage.googleapis.com/pieces-web-extensions-cdn/link.png)Share[https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png](https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png)Ask Copilot[https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png](https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png)

- **Subscription:** Represents a user's monthly subscription.

    - **Schema / Interface Definition (Conceptual):**

        TypeScript

        ```text
        interface Subscription {
          id: string; // Unique identifier for the subscription.
          userId: string; // Foreign key to User.
          status: "active" | "inactive" | "pending" | "cancelled"; // Current status.
          startDate: Date; // Date subscription started.
          endDate: Date; // Date subscription ends (for current cycle).
          nextBillingDate: Date; // Next automated billing date.
          paymentMethodId: string; // Reference to payment method.
          // ... other subscription-related properties
        }
        ```

        [https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png](https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png)Copy And Save[https://storage.googleapis.com/pieces-web-extensions-cdn/link.png](https://storage.googleapis.com/pieces-web-extensions-cdn/link.png)Share[https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png](https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png)Ask Copilot[https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png](https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png)

- **VirtualWallet:** Represents a user's virtual coin balance and history.

    - **Schema / Interface Definition (Conceptual):**

        TypeScript

        ```text
        interface VirtualWallet {
          id: string; // Unique identifier for the wallet.
          userId: string; // Foreign key to User.
          currentBalance: number; // Current virtual coin balance.
          lastCoinDistributionDate: Date; // Date of last monthly coin deposit.
          // ... other wallet-related properties
        }
        ```

        [https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png](https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png)Copy And Save[https://storage.googleapis.com/pieces-web-extensions-cdn/link.png](https://storage.googleapis.com/pieces-web-extensions-cdn/link.png)Share[https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png](https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png)Ask Copilot[https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png](https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png)

- **CoinTransaction:** Represents a single transaction affecting the virtual wallet.

    - **Schema / Interface Definition (Conceptual):**

        TypeScript

        ```text
        interface CoinTransaction {
          id: string; // Unique identifier.
          walletId: string; // Foreign key to VirtualWallet.
          type: "deposit" | "prediction_place" | "prediction_win" | "bonus" | "reset"; // Type of transaction.
          amount: number; // Amount of coins involved.
          timestamp: Date; // Time of transaction.
          referenceId?: string; // Optional: ID of associated prediction, bonus, etc.
          description: string; // Human-readable description.
        }
        ```

        [https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png](https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png)Copy And Save[https://storage.googleapis.com/pieces-web-extensions-cdn/link.png](https://storage.googleapis.com/pieces-web-extensions-cdn/link.png)Share[https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png](https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png)Ask Copilot[https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png](https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png)

- **SportingEvent:** Represents an upcoming or completed sporting event.

    - **Schema / Interface Definition (Conceptual):**

        TypeScript

        ```text
        interface SportingEvent {
          id: string; // Unique identifier (e.g., from external API).
          externalId: string; // ID from external data source.
          sportType: string; // e.g., 'Soccer', 'Basketball'.
          homeTeam: string; // Name of home team/participant.
          awayTeam: string; // Name of away team/participant.
          startTime: Date; // UTC start time of the event.
          status: "upcoming" | "live" | "completed" | "cancelled"; // Event status.
          winner?: string; // Name of the winning team/participant (for completed events).
          currentScore?: { home: number; away: number; }; // For live updates.
          // ... other event-specific properties
        }
        ```

        [https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png](https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png)Copy And Save[https://storage.googleapis.com/pieces-web-extensions-cdn/link.png](https://storage.googleapis.com/pieces-web-extensions-cdn/link.png)Share[https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png](https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png)Ask Copilot[https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png](https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png)

- **Odds:** Represents the odds for a specific outcome of a sporting event.

    - **Schema / Interface Definition (Conceptual):**

        TypeScript

        ```text
        interface Odds {
          id: string; // Unique identifier.
          eventId: string; // Foreign key to SportingEvent.
          outcome: string; // e.g., 'Home Win', 'Away Win', 'Draw'.
          value: number; // The odds value (e.g., 1.5, 2.75).
          lastUpdated: Date; // Timestamp of when odds were last updated.
          // ... other odds-specific properties
        }
        ```

        [https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png](https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png)Copy And Save[https://storage.googleapis.com/pieces-web-extensions-cdn/link.png](https://storage.googleapis.com/pieces-web-extensions-cdn/link.png)Share[https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png](https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png)Ask Copilot[https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png](https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png)

- **Prediction:** Represents a user's placed prediction on a sporting event.

    - **Schema / Interface Definition (Conceptual):**

        TypeScript

        ```text
        interface Prediction {
          id: string; // Unique identifier.
          userId: string; // Foreign key to User.
          eventId: string; // Foreign key to SportingEvent.
          predictedOutcome: string; // User's chosen outcome (e.g., 'Home Win').
          coinsPlaced: number; // Amount of virtual coins placed.
          oddsAtPrediction: number; // Odds at the moment the prediction was placed.
          status: "pending" | "won" | "lost" | "cancelled"; // Outcome status.
          winnings?: number; // Coins won if prediction is correct.
          timestamp: Date; // Time prediction was placed.
          // ... other prediction-related properties
        }
        ```

        [https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png](https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png)Copy And Save[https://storage.googleapis.com/pieces-web-extensions-cdn/link.png](https://storage.googleapis.com/pieces-web-extensions-cdn/link.png)Share[https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png](https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png)Ask Copilot[https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png](https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png)

- **LeaderboardEntry:** Represents a user's position on the monthly leaderboard.

    - **Schema / Interface Definition (Conceptual):**

        TypeScript

        ```text
        interface LeaderboardEntry {
          userId: string; // Foreign key to User.
          month: string; // e.g., '2025-06'.
          currentCoinTotal: number; // User's current coin total for the month.
          rank: number; // User's current rank.
          // ... other leaderboard-related metrics
        }
        ```

        [https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png](https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png)Copy And Save[https://storage.googleapis.com/pieces-web-extensions-cdn/link.png](https://storage.googleapis.com/pieces-web-extensions-cdn/link.png)Share[https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png](https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png)Ask Copilot[https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png](https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png)

- **NewsArticle:** Represents a sports news article.

    - **Schema / Interface Definition (Conceptual):**

        TypeScript

        ```text
        interface NewsArticle {
          id: string; // Unique identifier.
          title: string;
          summary: string;
          imageUrl?: string;
          fullContent: string; // Hosted within Sportsclub.
          sourceUrl?: string; // Original source if scraped.
          publishDate: Date;
          sportType?: string; // Optional: related sport.
          articleType: "news" | "pre_game_analysis" | "post_game_analysis" | "educational";
        }
        ```

        [https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png](https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png)Copy And Save[https://storage.googleapis.com/pieces-web-extensions-cdn/link.png](https://storage.googleapis.com/pieces-web-extensions-cdn/link.png)Share[https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png](https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png)Ask Copilot[https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png](https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png)

- **ForumPost:** Represents a post in the community forum.

    - **Schema / Interface Definition (Conceptual):**

        TypeScript

        ```text
        interface ForumPost {
          id: string;
          authorId: string; // Foreign key to User.
          categoryId: string; // Forum category.
          title: string;
          content: string; // Supports text, links, images.
          upvotes: number;
          downvotes: number;
          createdAt: Date;
          lastUpdated?: Date;
          // ... other post-related properties
        }
        ```

        [https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png](https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png)Copy And Save[https://storage.googleapis.com/pieces-web-extensions-cdn/link.png](https://storage.googleapis.com/pieces-web-extensions-cdn/link.png)Share[https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png](https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png)Ask Copilot[https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png](https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png)

- **ForumComment:** Represents a comment on a forum post.

    - **Schema / Interface Definition (Conceptual):**

        TypeScript

        ```text
        interface ForumComment {
          id: string;
          postId: string; // Foreign key to ForumPost.
          authorId: string; // Foreign key to User.
          content: string;
          upvotes: number;
          downvotes: number;
          createdAt: Date;
          // ... other comment-related properties
        }
        ```

        [https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png](https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png)Copy And Save[https://storage.googleapis.com/pieces-web-extensions-cdn/link.png](https://storage.googleapis.com/pieces-web-extensions-cdn/link.png)Share[https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png](https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png)Ask Copilot[https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png](https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png)

- **ChatMessage:** Represents a message in a live event chat.

    - **Schema / Interface Definition (Conceptual):**

        TypeScript

        ```text
        interface ChatMessage {
          id: string;
          eventId: string; // Foreign key to SportingEvent (for live chat).
          senderId: string; // Foreign key to User or 'AI'.
          content: string;
          timestamp: Date;
          type: "user" | "ai" | "system_update"; // e.g., for score updates.
          // ... other chat-related properties
        }
        ```

        [https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png](https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png)Copy And Save[https://storage.googleapis.com/pieces-web-extensions-cdn/link.png](https://storage.googleapis.com/pieces-web-extensions-cdn/link.png)Share[https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png](https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png)Ask Copilot[https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png](https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png)

- **GamificationActivity:** Represents a record of a gamified action or bonus.

    - **Schema / Interface Definition (Conceptual):**

        TypeScript

        ```text
        interface GamificationActivity {
          id: string;
          userId: string;
          type: "daily_bonus" | "login_streak" | "win_streak" | "community_challenge";
          value: number; // e.g., bonus coins awarded.
          timestamp: Date;
          streakCount?: number; // For streak bonuses.
          challengeId?: string; // For community challenges.
        }
        ```

        [https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png](https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png)Copy And Save[https://storage.googleapis.com/pieces-web-extensions-cdn/link.png](https://storage.googleapis.com/pieces-web-extensions-cdn/link.png)Share[https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png](https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png)Ask Copilot[https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png](https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png)

- **Discussion on Microservice Database Strategy (Your Question):**

    - The principle of "database per service" is indeed a common best practice in microservices to ensure loose coupling, independent scalability, and technological diversity for each service. This helps avoid a single database bottleneck and allows each service to optimize its persistence layer.

    - Solutions like **Turso (SQLite on the edge, via libSQL) or Neon (serverless PostgreSQL)** are excellent choices for modern, highly performant, and potentially geo-distributed data needs, especially if specific microservices require very low-latency reads or serverless scaling.

    - **Decision for Sportsclub:** While our initial "Technical Assumptions" specified PostgreSQL as the primary relational database, the architecture will embrace the **"database per service" principle** where appropriate. This means that while PostgreSQL (managed, scalable cloud instances) will be the *default* and *primary* choice for services requiring robust relational data, individual microservices (e.g., a specific leaderboard service, a highly transactional prediction service) may leverage alternative database technologies (like Turso or Neon for specialized needs, or Redis for caching/transient data) if a clear performance, scalability, or operational benefit is identified that outweighs the added complexity of managing multiple database types. This decision will be made on a service-by-service basis during detailed design.

- **Data Access Patterns:** Data access will primarily be facilitated through a **Repository Pattern** to abstract data storage concerns from business logic. ORM (Object-Relational Mapping) will be preferred for common CRUD operations where applicable (e.g., using Drizzle ORM).

- **Data Migration & Seeding:** Database schema changes will be managed using a **database migration tool** (e.g., integrated with Drizzle ORM's migration capabilities, or a standalone tool) to ensure iterative and version-controlled schema evolution. A **seeding approach** will be used to populate development and testing environments with initial or dummy data.

## Core Workflow / Sequence Diagrams

This section illustrates key or complex workflows using Mermaid sequence diagrams. These diagrams will help visualize interactions between different services and components.

### Example: User Places a Prediction (High-Level)

Code snippet

```text
sequenceDiagram
    participant FE as Frontend Web App
    participant GW as API Gateway
    participant US as Auth & User Service
    participant PS as Prediction Engine Service
    participant DI as Data Ingestion & Validation Service
    participant DB as PostgreSQL/Redis
    FE->>GW: 1. User navigates to Event Listings
    GW->>PS: 2. Request current Major Sporting Events & Odds
    PS->>DI: 3. Fetch/Cache Events & Odds (from External APIs/Scraping)
    DI-->>PS: 4. Validated Events & Odds
    PS-->>GW: 5. Events & Odds Data
    GW-->>FE: 6. Display Events & Odds
    FE->>GW: 7. User submits Prediction (Event, Pick, Coins)
    GW->>US: 8. Validate User Session/Authentication
    US-->>GW: 9. User Authenticated
    GW->>PS: 10. Request to Place Prediction
    PS->>DB: 11. Deduct Coins from User Wallet (Transaction)
    DB-->>PS: 12. Coins Deducted
    PS->>DB: 13. Record Prediction
    DB-->>PS: 14. Prediction Recorded
    PS-->>GW: 15. Prediction Confirmation
    GW-->>FE: 16. In-App Prediction Confirmation
    Note over PS, DI: Event Concludes (External Trigger)
    DI->>PS: 17. Official Event Outcome & Scores Received (validated)
    PS->>DB: 18. Update Prediction Status (Win/Loss) & Calculate Winnings
    PS->>DB: 19. Credit Winnings to User Wallet (if won)
    PS->>DB: 20. Update Leaderboard
    PS->>GW: 21. Notify Leaderboard/User of Prediction Outcome (WebSocket Event)
    GW->>FE: 22. Real-time Leaderboard Update & In-App Notification
```

[https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png](https://storage.googleapis.com/pieces-web-extensions-cdn/pieces.png)Copy And Save[https://storage.googleapis.com/pieces-web-extensions-cdn/link.png](https://storage.googleapis.com/pieces-web-extensions-cdn/link.png)Share[https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png](https://storage.googleapis.com/pieces-web-extensions-cdn/copilot.png)Ask Copilot[https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png](https://storage.googleapis.com/pieces-web-extensions-cdn/settings.png)

### Example: AI Assistant Generates Data Visualization

![sportsclub-architecture-ai-data-visualization-sequence-mmd](../MediaFiles/Images/sportsclub-architecture-ai-data-visualization-sequence-mmd.svg)

[[sportsclub-architecture-ai-data-visualization-sequence-mmd]]

```text
sequenceDiagram
    participant FE as Frontend Web App
    participant GW as API Gateway
    participant AI as AI Assistant Service
    participant DB as Data Stores
    participant LLM as External LLM / AI Models
    FE->>GW: 1. User inputs query for data visualization (e.g., "Show Team X trends")
    GW->>AI: 2. Forward Query
    AI->>DB: 3. Fetch relevant sports data (team history, player stats)
    DB-->>AI: 4. Raw Data
    AI->>LLM: 5. Process Data / Generate Visualization Instructions (e.g., JSON config for chart)
    LLM-->>AI: 6. Visualization Instructions
    AI-->>GW: 7. Generated Visualization Data/Instructions
    GW-->>FE: 8. Display Loading Indicator
    FE->>FE: 9. Render Visualization using Instructions
    Note over FE: User analyzes visualization, may ask follow-up questions.
```

## Definitive Tech Stack Selections

This section outlines the definitive technology choices for the project. These selections should be made after a thorough understanding of the project's requirements, components, data models, and core workflows. The Architect Agent should guide the user through these decisions, ensuring each choice is justified and recorded accurately in the table below. This table is the **single source of truth** for all technology selections. Other architecture documents (e.g., Frontend Architecture) must refer to these choices and elaborate on their specific application rather than re-defining them.

Must be definitive selections; do not list open-ended choices (e.g., for web scraping, pick one tool, not two). Specify exact versions (e.g., `18.2.0`). If 'Latest' is used, it implies the latest stable version *at the time of this document's last update*, and the specific version (e.g., `xyz-library@2.3.4`) should be recorded. Pinning versions is strongly preferred to avoid unexpected breaking changes for the AI agent.

| **Category**        | **Technology**                                                | **Version / Details**                      | **Description / Purpose**                                                             | **Justification (Optional)**                                                           |
| :------------------ | :------------------------------------------------------------ | :----------------------------------------- | :------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------- |
| **Languages**       | TypeScript                                                    | 5.x (Latest Stable)                        | Primary language for frontend and shared services.                                    | Strong type safety, large ecosystem, supports modern web development.                  |
|                     | Python                                                        | 3.11+                                      | Primary language for backend microservices and AI/ML components.                      | Excellent for data processing, AI/ML libraries, FastAPI performance.                   |
| **Runtime**         | Node.js                                                       | 20.x (LTS)                                 | Server-side execution environment for Next.js.                                        | Next.js dependency.                                                                    |
| **Frameworks**      | Next.js                                                       | 14.x (Latest Stable)                       | Frontend UI framework for web application.                                            | Aligns with user preference, SSR/SSG capabilities, Vercel integration, performance.    |
|                     | FastAPI                                                       | Latest Stable                              | Backend API framework for microservices.                                              | Aligns with user preference, high performance, Python ecosystem, async support.        |
| **Databases**       | PostgreSQL                                                    | 16.x (Latest Stable)                       | Primary relational data store.                                                        | Aligns with user preference, robustness, reliability, data integrity, extensibility.   |
|                     | Redis                                                         | Latest Stable                              | Caching, session storage, real-time data (e.g., leaderboard updates).                 | Aligns with user preference, high performance, in-memory store.                        |
| **Cloud Platform**  | AWS / GCP                                                     | (Flexible for cost/free tier optimization) | Primary cloud providers for backend microservices.                                    | High scalability, comprehensive managed services, and free tier options.               |
| **Cloud Services**  | Vercel                                                        | N/A                                        | Frontend deployment and hosting.                                                      | Optimized for Next.js, streamlined deployments.                                        |
|                     | Cloudflare                                                    | N/A                                        | CDN, edge services (e.g., DNS, WAF, Workers).                                         | Frontend performance optimization, security, complementary to primary cloud.           |
|                     | (Specific Managed Services on AWS/GCP)                        | N/A                                        | E.g., AWS Lambda/ECS/EKS, RDS, SQS, SNS, GCP Cloud Functions/Run, Cloud SQL, Pub/Sub. | To be selected during detailed architectural design.                                   |
| **Infrastructure**  | Turborepo                                                     | Latest Stable                              | Monorepo management.                                                                  | Aligns with user preference, build caching, task orchestration.                        |
|                     | Docker                                                        | Latest Stable                              | Containerization for microservices.                                                   | Portability, consistent environments.                                                  |
|                     | (IaC Tool)                                                    | (TBD)                                      | Infrastructure as Code (e.g., AWS CDK, Terraform).                                    | Automation, version control for infrastructure.                                        |
| **AI/ML Libraries** | Optillm (or similar)                                          | Latest Stable                              | Reasoning enhancement for AI Assistant.                                               | Aligns with user preference.                                                           |
|                     | Agentic RAG                                                   | (Framework/Tool TBD)                       | Agentic Retrieval-Augmented Generation for AI Assistant.                              | Aligns with user preference, robust information retrieval.                             |
|                     | Graphiti (or similar)                                         | (Library/Tool TBD)                         | Incremental Knowledge Graph for AI Assistant.                                         | Aligns with user preference, enhanced AI reasoning.                                    |
|                     | Portkey (or similar)                                          | (Library/Tool TBD)                         | Prompt and response caching for LLM inference.                                        | Aligns with user preference, performance optimization for AI.                          |
| **Real-time Comms** | WebSockets (e.g., Socket.IO)                                  | Latest Stable                              | Real-time leaderboard updates and live chat.                                          | Persistent, low-latency communication.                                                 |
| **Web Scraping**    | Searxng, Tavily, Exa, Brave, Serp, AgentQL, Crawl4AI, Jina AI | (Specific Libraries/Integrations TBD)      | Agent-powered dynamic data acquisition.                                               | Flexible and broad coverage for external data.                                         |
| **Testing**         | (Frameworks/Libraries TBD)                                    | (Versions TBD)                             | Unit, Integration, E2E testing.                                                       | To be determined in comprehensive testing strategy.                                    |
| **CI/CD**           | GitHub Actions                                                | N/A                                        | Continuous Integration/Continuous Deployment.                                         | Common practice, integrates with GitHub repos.                                         |
| **ORM**             | Drizzle ORM                                                   | Latest Stable                              | Database ORM for PostgreSQL.                                                          | Aligns with user preference, type-safe query building.                                 |
| **Styling**         | Tailwind CSS                                                  | v4.x (Preferred)                           | Utility-first CSS framework.                                                          | Aligns with user preference, rapid UI development.                                     |
| **UI Components**   | Radix UI                                                      | Latest Stable                              | Headless UI component primitives.                                                     | Aligns with user preference, accessible, unstyled primitives for custom design system. |
| **Animation**       | Framer Motion, Anime.js                                       | Latest Stable                              | Frontend animation libraries.                                                         | Aligns with user preference, rich UI animations.                                       |

## Infrastructure and Deployment Overview

- **Cloud Provider(s):** AWS / GCP (for backend microservices and core infrastructure), Vercel (for Next.js frontend), Cloudflare (for CDN, edge services).

- **Core Services Used:** (Specific managed services on AWS/GCP to be selected during detailed architectural design, e.g., Lambda/ECS for compute, RDS/Cloud SQL for database, SQS/Pub/Sub for messaging, API Gateway).

- **Infrastructure as Code (IaC):** (Tool used - e.g., AWS CDK, Terraform... to be selected). Location: (Link to IaC code repo/directory - to be defined).

- **Deployment Strategy:** Continuous Integration/Continuous Deployment (CI/CD) pipeline with automated promotions. The Next.js frontend will leverage Vercel's integrated CI/CD. Backend microservices will utilize Docker containers and automated deployments on AWS/GCP.

- **Deployment Frequency:** On-demand and daily deployments targeted for the MVP.

- **Environments:** Development, Staging, Production.

- **Environment Promotion:** (Describe steps, e.g., `dev` -> `staging` (manual approval / automated tests pass) -> `production` (automated after tests pass and optional manual approval)).

- **Rollback Strategy:** (e.g., Automated rollback on health check failure post-deployment, Manual trigger via CI/CD job, IaC state rollback. Specify primary mechanism).

## Error Handling Strategy

This section outlines the general approach to error handling across the Sportsclub platform, covering both system-level mechanisms and user-facing experiences.

- **General Approach:** The system will utilize a consistent error handling approach, primarily based on exceptions for internal logic and clear error codes/messages for API responses. Custom error types will be defined for domain-specific errors to enhance clarity and maintainability.

- **Logging:**

    - **Library/Method:** Structured logging will be implemented using a suitable library (e.g., Python `logging` module with `structlog` for FastAPI, a dedicated logging library like `Pino` for Node.js).

    - **Format:** Log messages will be in JSON format for structured, machine-readable output, facilitating centralized logging and analysis.

    - **Levels:** Standard log levels (DEBUG, INFO, WARN, ERROR, CRITICAL) will be consistently applied, with specific usage guidelines for each level.

    - **Context:** All logs MUST include essential contextual information such as a correlation ID (for tracing requests across microservices), service name, operation name, and sanitized key parameters. Sensitive PII MUST NOT be logged.

- **Specific Handling Patterns:**

    - **External API Calls:** Robust retry mechanisms (e.g., exponential backoff with max retries) will be implemented for transient external API failures. Circuit breaker patterns may be applied to critical external dependencies to prevent cascading failures. Clear timeouts (connect and read) will be configured. External API errors (4xx, 5xx) will be translated into appropriate internal errors or user-facing messages.

    - **Internal Errors / Business Logic Exceptions:** Internal errors will be converted into generic, user-friendly error messages or unique error IDs for client display, preventing sensitive information leakage. Detailed error information (stack traces, internal details) will only be captured in server-side logs.

    - **Transaction Management:** Data consistency will be ensured using appropriate transaction management (e.g., database transactions with defined isolation levels). For distributed transactions across microservices, compensating transactions or event-driven sagas will be explored.

- **User-Facing Error Handling:** As stated in the UI/UX Specification, Sportsclub will strive for clear and helpful user-facing error handling. Error messages will be presented in plain language, avoid technical jargon, and whenever possible, offer constructive guidance to help users understand the issue and how to resolve it or retry an relevant action. The system will aim to prevent common errors and allow users to recover gracefully from issues where feasible.

## Coding Standards

These standards are mandatory for all code generation by AI agents and human developers. Deviations are not permitted unless explicitly approved and documented as an exception in this section or a linked addendum.

- **Primary Runtime(s):** Node.js 20.x (LTS) for Next.js, Python 3.11+ for FastAPI microservices.

- **Style Guide & Linter:**

    - **TypeScript/JavaScript:** ESLint with a widely adopted config (e.g., Airbnb) + Prettier for formatting.

    - **Python:** Black for formatting, Flake8 for linting, and MyPy for static type checking.

    - Linter rules are mandatory and must not be disabled without cause. Configuration files (e.g., `.eslintrc.js`, `pyproject.toml`) will be committed to the repository.

- **Naming Conventions:**

    - **Variables, Functions/Methods:** `camelCase` for TypeScript/JavaScript, `snake_case` for Python.

    - **Classes/Types/Interfaces:** `PascalCase`.

    - **Constants:** `UPPER_SNAKE_CASE`.

    - **Files:** `kebab-case.ts` (TypeScript), `snake_case.py` (Python). UI component files and directories will generally follow `kebab-case`.

    - **Modules/Packages:** `camelCase` (TypeScript/JavaScript), `snake_case` (Python).

- **File Structure:** Adhere to the monorepo layout defined in the "Project Structure" section, with detailed frontend structure in the Frontend Architecture Document.

- **Unit Test File Organization:** Unit test files (`*.test.ts`/`*.spec.ts` for JS/TS, `test_*.py` for Python) will be co-located with their source files or in a parallel `tests/` directory, following language conventions.

- **Asynchronous Operations:**

    - **TypeScript/JavaScript/Python:** Always use `async`/`await` for promise-based operations.

    - Ensure clear patterns for error propagation and handling in asynchronous flows.

- **Type Safety:** All new code must be strictly typed.

    - **TypeScript:** Leverage TypeScript strict mode (all flags enabled). Avoid `!` non-null assertion operator; prefer explicit checks, optional chaining (`?.`), or nullish coalescing (`??`).

    - **Python:** Utilize full type hints, enforced by MyPy in CI.

    - Type definitions will be located in shared packages or co-located with components/modules. Policy on using `any` (strongly discouraged, requires justification).

- **Comments & Documentation:**

    - **Code Comments:** Explain *why* (complex logic, design choices), not *what* (obvious code). Use standard formats like JSDoc/TSDoc for TypeScript, Python docstrings (e.g., Google/NumPy style).

    - **READMEs:** Each module/package/service should have a README explaining its purpose, setup, and usage if not trivial.

- **Dependency Management:** PNPM for JavaScript/TypeScript, PDM with uv for Python. Policy on adding new dependencies will include an approval process, checking for existing alternatives, and security vulnerability scans. Prefer pinned versions for stability.

- **API Documentation Standards:** All internal APIs exposed by microservices MUST be documented using a standard specification (e.g., OpenAPI/Swagger), enabling clear contracts for frontend and inter-service communication.

### Detailed Language & Framework Conventions

#### `TypeScript/Node.js` Specifics:

- **Immutability:** Always prefer immutable data structures. Use `Readonly<T>`, `ReadonlyArray<T>`, `as const` for object/array literals. Avoid direct mutation of objects/arrays passed as props or state.

- **Functional vs. OOP:** Favor functional programming constructs (map, filter, reduce, pure functions) for data transformation and business logic where practical. Use classes for entities, services with clear state/responsibilities, or when framework conventions (e.g., NestJS) demand.

- **Error Handling Specifics:** Always use `Error` objects or extensions thereof for `throw`. Ensure `Promise` rejections are always `Error` objects. Use custom error classes inheriting from a base `AppError` for domain-specific errors.

- **Null/Undefined Handling:** Strict null checks (`strictNullChecks`) must be enabled. Avoid `!` non-null assertion operator; prefer explicit checks, optional chaining (`?.`), or nullish coalescing (`??`). Define clear strategies for optional function parameters and return types.

- **Module System:** Use ESModules (`import`/`export`) exclusively. Avoid CommonJS (`require`/`module.exports`) in new code.

- **Logging Specifics:** Use the chosen structured logging library. Log messages must include a correlation ID. Do not log sensitive PII. Use appropriate log levels.

    - **Framework Idioms (Next.js):** Follow Next.js App Router conventions for routing, layouts, and data fetching.

- **Key Library Usage Conventions:** When using Axios, create a single configured instance. For date/time, use `date-fns`/`Luxon`/`Day.js` and avoid native `Date` object for manipulations.

- **Code Generation Anti-Patterns to Avoid:** Avoid overly nested conditional logic (max 2-3 levels). Avoid single-letter variable names (except for trivial loop counters). Do not write code that bypasses framework security features.

#### `Python` Specifics:

- **Immutability:** Use tuples for immutable sequences. For classes, consider `@dataclass(frozen=True)`. Be mindful of mutable default arguments.

- **Functional vs. OOP:** Employ classes for representing entities and services. Use functions for stateless operations. List comprehensions/generator expressions are preferred over `map`/`filter` for readability.

- **Error Handling Specifics:** Always raise specific, custom exceptions inheriting from a base `AppException`. Use `try-except-else-finally` blocks appropriately. Avoid broad `except Exception:` clauses without re-raising or specific handling.

- **Resource Management:** Always use `with` statements for resources like files or DB connections to ensure they are properly closed.

- **Type Hinting:** All new functions and methods must have full type hints. Run MyPy in CI. Strive for `disallow_untyped_defs = True`.

- **Logging Specifics:** Use the `logging` module configured for structured output (e.g., with `python-json-logger`). Include correlation IDs.

    - **Framework Idioms (FastAPI):** Utilize Pydantic for request/response models and dependency injection for services.

- **Key Library Usage Conventions:** For HTTP requests, use `httpx` or `requests` with explicit timeout settings. For data manipulation, prefer `pandas` where appropriate but be mindful of performance.

## Overall Testing Strategy

This section outlines the project's comprehensive testing strategy, which all AI-generated and human-written code must adhere to. It complements the testing tools listed in the "Definitive Tech Stack Selections".

- **Tools:** (To be determined. E.g., Jest, Playwright, PyTest, JUnit, Testcontainers for backend).

- **Unit Tests:**

    - **Scope:** Test individual functions, methods, classes, or small modules in isolation. Focus on business logic, algorithms, and transformation rules.

    - **Location:** `*.test.ts`/`*.spec.ts` (JS/TS) co-located with source files or `test_*.py` (Python) in a parallel `tests/` directory, following language conventions.

    - **Mocking/Stubbing:** Use appropriate mocking libraries (e.g., Jest mocks, `unittest.mock` in Python). Mock all external dependencies (network calls, file system, databases, time).

    - **AI Agent Responsibility:** AI Agent MUST generate unit tests covering all public methods, significant logic paths, edge cases, and error conditions for any new or modified code.

- **Integration Tests:**

    - **Scope:** Test the interaction between several components or services within the application boundary. E.g., API endpoint to service layer to database (using a test database or in-memory version).

    - **Location:** (To be defined, e.g., `/tests/integration`).

    - **Environment:** Dependencies handled (e.g., Testcontainers for databases/external services, in-memory databases, dedicated test environment).

    - **AI Agent Responsibility:** AI Agent MAY be tasked with generating integration tests for key service interactions or API endpoints based on specifications.

- **End-to-End (E2E) Tests:**

    - **Scope:** Validate complete user flows or critical paths through the system from the user's perspective (e.g., UI interaction, API call sequence).

    - **Tools:** (To be determined. E.g., Playwright, Cypress).

    - **AI Agent Responsibility:** AI Agent MAY be tasked with generating E2E test stubs or scripts based on user stories or BDD scenarios. Focus on critical happy paths and key error scenarios.

- **Test Coverage:**

    - **Target:** (To be defined. E.g., 80% line/branch coverage for unit tests). This is a guideline; quality of tests is paramount over raw coverage numbers.

    - **Measurement:** (Tool used for coverage reports, e.g., Istanbul/nyc, Coverage.py).

- **Mocking/Stubbing Strategy (General):** Prefer fakes or test doubles over extensive mocking where it improves test clarity and maintainability. Strive for tests that are fast, reliable, and isolated.

- **Test Data Management:** How is test data created, managed, and isolated? (e.g., factories, fixtures, setup/teardown scripts, dedicated test data generation tools).

- **Performance Testing:** Performance testing will be conducted against key Non-Functional Requirements (NFRs) (e.g., response times, capacity, scalability) to ensure the system meets performance benchmarks under expected and peak loads.

- **Security Testing:** Regular security testing, including automated vulnerability scans (SAST/DAST) and periodic penetration testing, will be integrated into the development lifecycle and CI/CD pipeline.

## Security Best Practices

This section outlines key security considerations relevant to the codebase. These are mandatory and must be actively addressed by the AI agent during development.

- **Input Sanitization/Validation:** All external inputs (API requests, user-provided data, file uploads) MUST be sanitized and validated at the boundary before processing. Use appropriate libraries and define clear schemas and constraints.

- **Output Encoding:** Output encoding must be performed where necessary to prevent XSS and other injection attacks. All dynamic data rendered in HTML templates must be contextually auto-escaped.

- **Secrets Management:** Secrets MUST NOT be hardcoded or included in source control. Access secrets ONLY through a designated secure configuration module/service. Use specific tools for local development (e.g., .env files NOT committed).

- **Dependency Security:** Automated vulnerability scans (e.g., `npm audit`, `pip-audit`, Snyk, Dependabot alerts) MUST be integrated into CI and run regularly. High/critical vulnerabilities MUST be addressed promptly.

- **Authentication/Authorization Checks:** All API endpoints (except explicitly public ones) MUST enforce authentication using the central auth module/middleware. Authorization (permission/role checks) MUST be performed at the service layer or entry point for protected resources.

- **Principle of Least Privilege (Implementation):** Database connection users and IAM roles for cloud services MUST have only the necessary permissions for the specific resources they access.

- **API Security (General):** Enforce HTTPS for all communication. Implement rate limiting and throttling. Use standard HTTP security headers (e.g., CSP, HSTS).

- **Error Handling & Information Disclosure:** Error messages MUST NOT leak sensitive information (stack traces, internal paths) to the end-user. Log detailed errors server-side, provide generic messages or error IDs to the client.

- **Secure Communication (HTTPS):** All communication must use HTTPS. Mixed content (HTTP assets on HTTPS page) is forbidden.

- **Data Access Audit Trails:** Critical data access events (e.g., access to PII, financial data, or sensitive configurations) MUST be logged for audit purposes, ensuring traceability and accountability.

- **CSRF/XSS Prevention:** Cross-Site Request Forgery (CSRF) prevention will be implemented as a backend / API Gateway concern. Cross-Site Scripting (XSS) prevention measures are addressed via output encoding.

- **Network Security Design:** The network architecture will utilize private subnets, Virtual Private Clouds (VPCs) or equivalent, and network access controls (e.g., security groups, network ACLs) for isolation and protection of internal services and databases.

## Key Reference Documents

This section lists other essential documents that provide critical context or detailed specifications for the Sportsclub project. These documents complement the Architecture Document and ensure a complete understanding of the project's requirements and design.

- **Product Requirements Document (PRD):** `docs/prd.md`

    - *Description:* Defines the product's vision, goals, functional and non-functional requirements, and Epic structure.

- **UI/UX Specification:** `docs/ui-ux-spec.md`

    - *Description:* Details the user experience goals, information architecture, user flows, and visual design guidelines for the frontend.

- **Comprehensive Research Report:** `comprehensive_research_report.md`

    - *Description:* Provides overall market research, competitive analysis, and strategic positioning insights for Sportsclub.

- **Alternative Odds Prediction Markets Research:** `alternative_odds_prediction_markets.md`

    - *Description:* Research on various prediction market models and their underlying mechanisms.

- **Predictive Analysis Sports Research:** `predictive_analysis_sports_research.md`

    - *Description:* Research on methodologies and challenges in sports predictive analytics.

- **Sports APIs and Data Sources Research:** `sports_apis_data_sources.md`

    - *Description:* Evaluation of potential external APIs and data scraping strategies for sports data.

- **Legal Compliance Research:** `legal_compliance_research.md`

    - *Description:* Analysis of legal and regulatory aspects pertaining to skill-based contests, cash prizes, and online gaming.

## Change Log

| **Change**    | **Date**   | **Version** | **Description**                                                                            | **Author**             |
| :------------ | :--------- | :---------- | :----------------------------------------------------------------------------------------- | :--------------------- |
| Initial Draft | 2025-06-05 | 1.0         | First comprehensive draft of Sportsclub Architecture Document, covering all core sections. | Fred (Architect Agent) |

---
