# System Context Diagram Concept: uXPRT

## Diagram Description

This diagram outlines the main components and external entities interacting with the uXPRT system. It shows the user interacting with the core uXPRT application, which in turn communicates with the conversational agent team, an external web search service, and a database for storing generated artifacts and user data.

## Entities

- **User:** The primary actor using the uXPRT application (Startup founders, solopreneurs, small business owners, content creators, marketers).
- **uXPRT Application:** The core web application interface.
- **Conversational Agent Team:** A set of AI agents providing guidance and generating artifacts.
- **External Web Search:** A service used by the agents for research.
- **Database:** Stores user data, conversation history, and generated artifacts.

## Relationships

- User interacts with the uXPRT Application.
- uXPRT Application communicates with the Conversational Agent Team.
- Conversational Agent Team uses the External Web Search for information.
- uXPRT Application and Conversational Agent Team read from and write to the Database.

```mermaid
C4Context
    Person(user, "User", "Startup founders, solopreneurs, etc.")
    System(uxprt_app, "uXPRT Application", "Core web application for accessing agents and artifacts.")
    System(agent_team, "Conversational Agent Team", "AI agents guiding users and generating artifacts.")
    System(web_search, "External Web Search", "Provides research data to agents.")
    System(database, "Database", "Stores user data, conversations, and artifacts.")

    Rel(user, uxprt_app, "Uses")
    Rel(uxprt_app, agent_team, "Communicates with")
    Rel(agent_team, web_search, "Uses for research")
    Rel(uxprt_app, database, "Reads from and writes to")
    Rel(agent_team, database, "Reads from and writes to")
```
