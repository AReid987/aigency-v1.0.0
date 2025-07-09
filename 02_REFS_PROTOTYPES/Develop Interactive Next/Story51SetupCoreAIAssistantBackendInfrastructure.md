---
type: Page
collections: sportsclub backlog
title: 'Story 5.1: Set up Core AI Assistant Backend Infrastructure'
description: null
icon: null
createdAt: '2025-06-09T23:05:01.767Z'
creationDate: 2025-06-09 18:05
modificationDate: 2025-06-11 23:10
tags: [Story]
coverImage: null
---

# Story 5.1: Set up Core AI Assistant Backend Infrastructure

# Story 5.1: Set up Core AI Assistant Backend Infrastructure

## Status: Draft

## Story

- As a **developer**,

- I want to **set up the core backend infrastructure for the AI Assistant, including LLM integration, prompt/response caching, and initial knowledge graph capabilities**,

- so that **the foundation for intelligent user interaction and data insights is in place.**

## Acceptance Criteria (ACs)

1. A dedicated microservice (AI Assistant Service) is established for AI functionalities.

2. Basic integration with a Language Model (LLM) is configured.

3. A prompt/response caching mechanism (e.g., Portkey or similar) is integrated for LLM interactions.

4. An initial knowledge graph (e.g., Graphiti or similar) is set up for basic information retrieval and reasoning.

5. The AI Assistant Service can receive basic text queries and return responses from the LLM, demonstrating foundational Q&A capability.

6. The caching mechanism demonstrably stores and retrieves cached responses, reducing LLM calls for repeated queries.

7. The knowledge graph can store and retrieve simple facts, demonstrating initial reasoning enhancement.

8. The AI Assistant Service is configured with appropriate security measures for LLM API keys and data handling.

## Tasks / Subtasks

- [ ] Create `ai-assistant-service` directory within `packages/` if not already created.

- [ ] Set up basic FastAPI application within `ai-assistant-service`.

- [ ] Configure LLM integration (e.g., API client for OpenAI, Google Gemini, or local model setup).

- [ ] Integrate and configure prompt/response caching library (e.g., Portkey).

- [ ] Set up initial knowledge graph database (e.g., Neo4j, or a graph library within a relational DB if simpler for MVP) and initial data.

- [ ] Implement a basic endpoint in `ai-assistant-service` to receive a text query and return an LLM response.

- [ ] Implement caching logic for LLM responses.

- [ ] Implement basic knowledge graph query and retrieval.

- [ ] Configure security for LLM API keys and data within the service.

- [ ] Write basic unit tests for LLM integration, caching, and knowledge graph components.

## Dev Technical Guidance

This story is highly complex due to the nature of AI/ML integration. Prioritize getting the foundational components working end-to-end at a basic level before focusing on advanced features.

- **Dependency:** This story **depends on Epic 1** (foundational setup, including monorepo, cloud infrastructure, and CI/CD). It also implicitly depends on `shared-libs` for common utilities.

- **AI/ML Libraries:** Refer to "Definitive Tech Stack Selections" in the Architecture Document for AI/ML Libraries (Optillm, Agentic RAG, Graphiti, Portkey). For this story, focus on getting a minimal viable integration of LLM, caching (Portkey or similar), and knowledge graph (Graphiti or similar) working.

- **LLM Integration:** Choose an initial LLM (e.g., OpenAI's API, Google's Gemini API) and configure its client within the service.

- **Knowledge Graph (KG):** For initial setup, the knowledge graph will store facts as a collection of simple triples (Subject-Predicate-Object) or nodes and relationships. This will support basic information retrieval.

    - Example Conceptual Structure: `(Entity:Team {name: "Team A"})-[PLAYS_AGAINST]->(Entity:Team {name: "Team B"})` or `(Fact: "Player X scored Y points in Game Z")`.

    - *Note: This conceptual model will be formalized in the main Architecture Document's "Data Models" section as the knowledge graph evolves.*

- **Security:** Adhere to "Security Best Practices" for handling LLM API keys, user input to LLMs, and any sensitive data involved in prompt/response caching or the knowledge graph.

- **Error Handling:** Implement robust error handling for LLM API failures, rate limits, and knowledge graph queries as per the "Error Handling Strategy."

- **Prototyping/Spikes:** As identified in the "Risk Management & Practicality" section of the PO checklist, this area is complex. Consider allocating small "spike" tasks if significant unknowns emerge during initial setup for a specific technology choice.

- **Testing Guidance:**

    - **Approach:** Unit tests for individual LLM integration, caching logic, and knowledge graph components. Integration tests for the end-to-end query processing (frontend -> AI service -> LLM/KG -> response). Manual testing for factual accuracy, relevance, and adherence to "no prediction" rule.

    - **Special Considerations:** Security testing should focus on protecting LLM API keys, preventing prompt injection vulnerabilities, and ensuring secure data handling within caching and the knowledge graph. Performance testing should include evaluating the effectiveness of caching in reducing LLM latency and cost.

## Story Progress Notes

### Agent Model Used: Bob (SM Agent)

### Completion Notes List

- (To be filled by Developer Agent upon completion)

### Change Log

- (To be filled by Developer Agent upon completion)


