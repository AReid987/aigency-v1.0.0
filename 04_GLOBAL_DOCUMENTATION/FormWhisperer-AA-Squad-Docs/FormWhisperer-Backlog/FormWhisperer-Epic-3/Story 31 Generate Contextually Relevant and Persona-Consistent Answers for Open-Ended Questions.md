---
type: Page
title: 'Story 3.1: Generate Contextually Relevant and Persona-Consistent Answers for Open-Ended Questions'
description: null
icon: null
createdAt: '2025-07-11T09:38:52.740Z'
creationDate: 2025-07-11 04:38
modificationDate: 2025-07-11 04:39
tags: []
coverImage: null
---

# Story 3.1: Generate Contextually Relevant and Persona-Consistent Answers for Open-Ended Questions

## Status: Draft

## Story

- As a FormWhisperer agent

- I want to generate contextually relevant and persona-consistent answers for open-ended survey questions

- so that I can complete qualitative sections of a survey authentically.

## Acceptance Criteria (ACs)

- The agent can parse an open-ended question prompt.

- The agent generates a textual response (minimum X characters, maximum Y characters, where X, Y are configurable) based on the current persona's profile and the question context.

- The generated response maintains the persona's established tone and opinion where applicable.

- The system logs the generated response and the question it answered.

- Local command-line test script can simulate open-ended questions and verify response generation.

## Tasks / Subtasks

- [ ] **Task 1: Design Response Generation Logic (AC: 1, 2, 3)**

    - [ ] Subtask 1.1: Create a new Python agent: `src/agents/response-generator/`.

    - [ ] Subtask 1.2: Implement a core function within `response-generator` that takes an open-ended question, current context (e.g., previous answers in the survey), and the active `Persona` object (from `docs/data-models.md`) as input.

    - [ ] Subtask 1.3: Integrate with a Large Language Model (LLM) using `LangChain` (Python) as per `docs/tech-stack.md`.

    - [ ] Subtask 1.4: Develop a prompt engineering strategy to instruct the LLM to generate responses:

        - Consistently with the `Persona`'s `demographics`, `preferences`, and `opinions`.

        - Adhering to the `responseStyle` (verbosity, tone) defined in the `Persona` schema.

        - Considering the `question` and `context` provided.

    - [ ] Subtask 1.5: Implement logic to enforce minimum and maximum character limits (X, Y configurable, initially define reasonable defaults like 50-200 characters) for generated responses.

- [ ] **Task 2: Integrate with Persona Service (AC: 2, 3)**

    - [ ] Subtask 2.1: Implement logic within `response-generator` to securely retrieve persona data from the `Persona Service` via its internal API (`docs/api-reference.md#persona-service-api`).

    - [ ] Subtask 2.2: Ensure the persona data is correctly formatted and passed to the LLM prompting process.

- [ ] **Task 3: Orchestrate Response Generation for Text Fields (AC: 1, 2)**

    - [ ] Subtask 3.1: Update the `automation-orchestrator` service (`src/services/automation-orchestrator/`) to call the `response-generator` for answers to open-ended text fields.

    - [ ] Subtask 3.2: Ensure the orchestrator passes the parsed question and current survey context (if available) from the `form-parser` to the `response-generator`.

    - [ ] Subtask 3.3: The orchestrator then uses the generated answer to instruct the `browser-automator` to fill the field (building on Story 2.1).

- [ ] **Task 4: Implement Robust Logging (AC: 4)**

    - [ ] Subtask 4.1: Ensure the `response-generator` logs the open-ended question received, the persona used, the generated response, and any LLM API calls/responses, adhering to `docs/operational-guidelines.md#logging` (structured JSON, `structlog`).

- [ ] **Task 5: Develop Local Test Script (AC: 5)**

    - [ ] Subtask 5.1: Create a Python CLI script (in `scripts/`) that allows a user to input a simulated open-ended question and select a persona ID.

    - [ ] Subtask 5.2: The script should call the `response-generator` function directly and display the generated answer, verifying its adherence to length constraints and basic persona consistency.

## Dev Technical Guidance

This story is foundational for FormWhisperer's core AI intelligence, focusing on the `Response Generator` component.

- **LLM Integration:** Use `LangChain` (Python) for interacting with the chosen LLM API (e.g., Gemini, OpenAI GPT) as specified in `docs/tech-stack.md`. Refer to `docs/api-reference.md#large-language-model-llm-api` for endpoint details.

- **Persona Data Usage:** The `Persona` data model (`docs/data-models.md#persona`) is critical. Ensure all relevant persona attributes (demographics, preferences, opinions, responseStyle) are effectively incorporated into the LLM prompt to guide response generation. The `Persona Service API` (`docs/api-reference.md#persona-service-api`) provides the interface for retrieving this data.

- **Prompt Engineering:** The quality of the generated answers will depend heavily on effective prompt engineering. Experiment with different prompt structures to achieve contextual relevance, persona consistency, and adherence to stylistic requirements. Consider few-shot examples within prompts if applicable.

- **Project Structure:** The new `response-generator` agent must be located in `src/agents/response-generator/` and adhere to the Python project structure. Updates to the `automation-orchestrator` are in `src/services/automation-orchestrator/`.

- **Logging & Security:** Implement structured logging (`structlog`) for all `response-generator` operations, capturing inputs and outputs, while strictly adhering to `docs/operational-guidelines.md#security-best-practices` to avoid logging sensitive PII or LLM API keys.

- **Coding Standards & Testing:** Adhere to Python coding standards, type hints, and unit test file organization as defined in `docs/operational-gudelines.md`.

    - Unit tests for `response-generator`: Focus on prompt construction, persona data integration, response length enforcement, and basic mock LLM responses.

    - Integration tests: Verify `response-generator` can successfully query a *mocked* LLM and retrieve persona data from the Persona Service.

## Story Progress Notes

### Agent Model Used: Benjamin "Beacon" Hayes (PO)

### Completion Notes List

### Change Log

