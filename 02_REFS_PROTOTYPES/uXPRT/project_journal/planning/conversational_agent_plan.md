# Plan: Conversational Agent Guidance Logic

**Task ID:** TASK-AI-20250503-235159

## 🎯 Objective

This plan outlines the architecture and key components for the conversational agent guidance logic within the uXPRT project. The primary goal is to enable the agent to effectively guide users through the UX pipeline, assist in the generation of project artifacts, and integrate seamlessly with other system components, fulfilling the requirements outlined in `project_journal/planning/requirements.md` and addressing the needs of the user personas defined in `project_journal/planning/user_personas.md`.

## 🏗️ Architecture Overview

The conversational agent logic will be implemented as a backend service, likely integrated into the main API layer built with Python/FastAPI, as suggested by the project constraints. This service will be responsible for processing user input, managing conversation state, interacting with other backend services for artifact generation and data handling, and generating appropriate responses for the user interface.

A high-level architecture could involve:

- **API Gateway:** Entry point for frontend requests.
- **Conversational Agent Service:** Core logic for dialogue management, NLU, and response generation.
- **Artifact Generation Services:** Dedicated services/modules for generating specific artifacts (PRD, personas, diagrams, etc.).
- **Data Handling Service:** Manages interaction with the database (Supabase).
- **Web Search Service:** Integrates with external search capabilities.

## ✨ Key Components

1.  **Natural Language Understanding (NLU) Module:**

    - Parses user input to identify intent (e.g., "define personas", "generate PRD") and extract relevant entities (e.g., project name, target audience details).
    - May leverage a pre-trained model or a custom-trained model based on expected user interactions within the UX pipeline.

2.  **Dialogue Management (DM) Module:**

    - Manages the state of the conversation, tracking user progress through the UX pipeline steps.
    - Determines the agent's next action based on user intent, current state, and available context.
    - Guides the user through necessary information gathering steps before triggering artifact generation.
    - Handles interruptions and context switching.

3.  **Knowledge Base / Context Engine:**

    - Stores information about the user's current project, previously provided details, generated artifacts, and the overall structure of the UX pipeline.
    - Provides context to the DM and Response Generation modules.

4.  **Backend Services Integration Layer:**

    - Acts as an interface between the DM module and other backend services.
    - Sends requests to Artifact Generation Services with necessary data.
    - Interacts with the Data Handling Service to save/retrieve project data and generated artifacts.
    - Communicates with the Web Search Service for research queries.

5.  **Response Generation Module:**
    - Formulates natural language responses for the user, providing guidance, asking clarifying questions, confirming actions, and presenting results.
    - Responses should be tailored to the user's current context and progress.

## 🤝 Integration Points

- **Data Handling:** The agent service will interact with the Data Handling Service to:

  - Save user input and conversation history.
  - Store parameters and data collected for artifact generation.
  - Retrieve existing project data and artifacts.
  - Manage user account information related to artifact access and versioning. Integration will likely involve API calls to the Data Handling Service, which in turn interacts with Supabase.

- **Artifact Generation:** The agent service will trigger specific Artifact Generation Services based on user requests and collected information. This will involve sending structured data to these services via internal API calls. The agent will then receive confirmation or the generated artifact data back from these services.

- **Web Search:** The agent will integrate with the Web Search Service to perform research on behalf of the user, especially during early stages like defining target demographics or understanding market trends, as highlighted in the user personas. The agent will formulate search queries and present relevant results to the user within the conversation flow.

## 🚶 UX Pipeline Guidance Flow

The agent will guide users sequentially or non-sequentially through the key features outlined in the requirements, corresponding to steps in the UX pipeline:

1.  **Project Initialization & Goal Setting:** Help the user define the basic project idea and objectives.
2.  **Target Demographic & User Personas:** Guide the user in identifying their target audience and creating detailed user personas, potentially using the Web Search integration for market data.
3.  **Product Documentation:** Assist in generating PRD, FRD, DRD, and ERD drafts by asking relevant questions and feeding the information to the respective generation services.
4.  **Diagrams, Wireframes, Sitemaps:** Guide the user through the process of creating these visual artifacts.
5.  **Business & Brand Assets:** Help develop GTM strategy, Lean Canvas, Brand Voice & Tone, Brand Identity, and Brand Book.

The DM module will track which steps are completed and suggest the next logical steps, while also allowing users to revisit or skip steps.

## 🛠️ Artifact Generation Assistance

The agent's role in artifact generation is primarily facilitative:

- **Information Gathering:** The agent will ask the user for all necessary information required by the specific artifact generation service.
- **Triggering Generation:** Once sufficient information is gathered, the agent will call the appropriate backend service to generate the artifact.
- **Presenting Results:** The agent will inform the user when the artifact is ready and provide access (e.g., a link to download or view within the app).
- **Iteration:** The agent can facilitate revisions by allowing users to provide feedback and trigger regeneration with updated parameters.

## ➡️ Future Considerations

- Implementing more sophisticated NLU for better understanding of complex or ambiguous user requests.
- Developing more dynamic and flexible dialogue flows that adapt more intelligently to user needs.
- Integrating with the Google ADK for potentially leveraging advanced AI models for conversation and artifact generation.
- Adding support for a wider range of artifact types.
- Implementing versioning and comparison features for generated artifacts with agent assistance.

This plan provides a foundation for implementing the conversational agent guidance logic, focusing on core components, integration points, and the user journey through the UX pipeline.
